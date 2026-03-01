from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
def predict(data: StudentInput):

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