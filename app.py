from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import requests
import os

security = HTTPBearer()

COGNITO_REGION = os.environ.get("COGNITO_REGION")
USER_POOL_ID = os.environ.get("USER_POOL_ID")
APP_CLIENT_ID = os.environ.get("APP_CLIENT_ID")

JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
jwks = requests.get(JWKS_URL).json()

def verify_token(token=Depends(security)):
    try:
        token_value = token.credentials
        headers = jwt.get_unverified_header(token_value)
        key = next(k for k in jwks["keys"] if k["kid"] == headers["kid"])

        payload = jwt.decode(
            token_value,
            key,
            algorithms=["RS256"],
            audience=APP_CLIENT_ID
        )
        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentInput(BaseModel):
    engagement_slope: float
    volatility_index: float
    fragmentation_score: float
    concept_failure_rate: float

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/predict")
def predict(data: StudentInput, user=Depends(verify_token)):

    # Dummy logic for now
    risk_score = (
        abs(data.engagement_slope) +
        data.volatility_index +
        data.fragmentation_score +
        data.concept_failure_rate
    ) / 4

    if risk_score > 0.6:
        risk_level = "High"
    elif risk_score > 0.3:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "top_factors": [
            "Engagement decline",
            "Performance volatility",
            "Concept gaps"
        ]
    }
