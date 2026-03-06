from fastapi import FastAPI,Request
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (simplest for hackathon)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BUCKET_NAME = "s3datasetbucket"
MODEL_KEY = "dropout_xgb_model.pkl"
LOCAL_MODEL_PATH = "/tmp/dropout_xgb_model.pkl"
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
    payload = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
    )
    return payload
    
def download_model():
    if not os.path.exists(LOCAL_MODEL_PATH):
        s3 = boto3.client("s3", region_name="ap-south-1")
        s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)

download_model()
model = joblib.load(LOCAL_MODEL_PATH)
explainer = shap.TreeExplainer(model)
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
        messages=[{
            "role": "user",
            "content": [{"text": prompt}]
        }],
        inferenceConfig={"maxTokens": 400}
    )
    return response["output"]["message"]["content"][0]["text"]
   
sns = boto3.client("sns", region_name="ap-south-1")
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:744861800308:dropout-alert-topic"
@app.post("/predict")
def predict(student: StudentInput, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"error": "Missing Authorization header"}
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    student_email = payload["email"]
    
    input_df = pd.DataFrame([student.dict()])
    prob = float(model.predict_proba(input_df)[0][1])

    if prob > 0.75:
        risk = "High"
    elif prob > 0.4:
        risk = "Moderate"
    else:
        risk = "Low"

    shap_values = explainer.shap_values(input_df)
    shap_array = shap_values[0]
    feature_names = input_df.columns.tolist()
    shap_pairs = list(zip(feature_names, shap_array))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_features = [f[0] for f in shap_pairs[:3]]

    narrative = call_bedrock(prob, risk, top_features, shap_pairs)

    if prob > 0.75:
        student_name = payload.get("name", "Student")
        message = f"""
        Hello {student_name},
        
        Our AI learning system detected that you may need additional academic support.
        
        Dropout Risk Probability: {prob:.2f}
        
        Recommended actions:
        • Review recent course materials
        • Practice weak concepts
        • Reach out to your instructor for guidance
        
        Keep going — improvement is always possible.
        """
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Learning Support Alert",
            Message=message
        )
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