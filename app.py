from fastapi import FastAPI, Request
from jose import jwt
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import boto3
import os
import shap
import numpy as np
import pandas as pd
import json

app = FastAPI()

origins = [
    "https://s3datasetbucket.s3.ap-south-1.amazonaws.com",
    "http://localhost:3000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BUCKET_NAME = "s3datasetbucket"
COGNITO_REGION = "ap-south-1"
USER_POOL_ID = "ap-south-1_3jHoa6lMn"
CLIENT_ID = "2uiog0l5j4v9flu4ifk5efea2n"
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
jwks = requests.get(JWKS_URL).json()

def verify_token(token):
    headers = jwt.get_unverified_header(token)
    key = None
    for k in jwks["keys"]:
        if k["kid"] == headers["kid"]:
            key = k
    if key is None:
        raise Exception("Public key not found")
    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}",
        options={"verify_at_hash": False}
    )
    return payload

LOCAL_MODEL_PATH  = "/tmp/dropout_rf_model.pkl"
LOCAL_SCALER_PATH = "/tmp/dropout_scaler.pkl"
LOCAL_SHAP_PATH   = "/tmp/dropout_shap_rf.pkl"

def download_models():
    s3 = boto3.client("s3", region_name="ap-south-1")
    if not os.path.exists(LOCAL_MODEL_PATH):
        print("Downloading RF model from S3...")
        s3.download_file(BUCKET_NAME, "dropout_rf_model.pkl", LOCAL_MODEL_PATH)
    if not os.path.exists(LOCAL_SCALER_PATH):
        print("Downloading scaler from S3...")
        s3.download_file(BUCKET_NAME, "dropout_scaler.pkl", LOCAL_SCALER_PATH)
    if not os.path.exists(LOCAL_SHAP_PATH):
        print("Downloading SHAP explainer from S3...")
        s3.download_file(BUCKET_NAME, "dropout_shap_rf.pkl", LOCAL_SHAP_PATH)

download_models()

model     = joblib.load(LOCAL_MODEL_PATH)
scaler    = joblib.load(LOCAL_SCALER_PATH)
explainer = joblib.load(LOCAL_SHAP_PATH)

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

class StudentInput(BaseModel):
    median_engagement: float
    recent_7d_median_engagement: float
    engagement_cv: float
    engagement_slope_14d: float
    median_submission_delay: float
    tab_switch_p75: float
    median_first_attempt_accuracy: float
    longest_drop_streak: int
    median_overall_accuracy: float
    trimmed_avg_response_time: float
    total_attempts: int
    weighted_concept_failure: float
    worst_concept_failure: float
    concept_variability: float

def call_bedrock(prob, risk, top_features, shap_pairs):
    drivers_text = "\n".join(
        [f"- {name}: SHAP value {value:.4f}" for name, value in shap_pairs[:5]]
    )
    prompt = f"""You are an educational psychologist and student support advisor.
A student has been flagged by an AI behavioral analysis system with the following results:
Dropout Risk Probability: {prob:.2f} ({risk} Risk)
Top behavioral drivers contributing to this risk:
{drivers_text}
Based on this analysis, write a clear, empathetic, and actionable intervention recommendation.
Your response should:
1. Briefly explain what the behavioral signals suggest about the student
2. Give 2-3 specific, practical recommendations for the educator
3. Give 1 encouraging message for the student themselves
Keep the tone warm, professional, and constructive. Avoid technical jargon."""
    response = bedrock.converse(
        modelId="global.amazon.nova-2-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 400}
    )
    return response["output"]["message"]["content"][0]["text"]

@app.post("/predict")
def predict(student: StudentInput, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"error": "Missing Authorization header"}
    token = auth_header.split(" ")[1]
    payload = verify_token(token)

    input_df = pd.DataFrame([student.dict()])
    input_scaled = scaler.transform(input_df)
    input_scaled_df = pd.DataFrame(input_scaled, columns=input_df.columns)

    prob = float(model.predict_proba(input_scaled)[0][1])
    if prob > 0.75:
        risk = "High"
    elif prob > 0.4:
        risk = "Moderate"
    else:
        risk = "Low"

    shap_vals = explainer.shap_values(input_scaled_df)
    if isinstance(shap_vals, list):
        shap_arr = shap_vals[1][0]
    else:
        shap_arr = shap_vals[:, :, 1][0] if shap_vals.ndim == 3 else shap_vals[0]

    feature_names = input_df.columns.tolist()
    shap_pairs = list(zip(feature_names, shap_arr))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_features = [f[0] for f in shap_pairs[:3]]

    narrative = call_bedrock(prob, risk, top_features, shap_pairs)

    return {
        "dropout_probability": prob,
        "risk_category": risk,
        "top_drivers": top_features,
        "shap_scores": {name: float(val) for name, val in shap_pairs[:5]},
        "intervention": narrative
    }

@app.get("/")
def home():
    return {"status": "Behavioral AI backend running"}
