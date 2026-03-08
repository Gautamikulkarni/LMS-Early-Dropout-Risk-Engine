# LMS Early Dropout Risk Engine

An AI-powered early warning system designed to identify students at risk of disengagement or dropout in Learning Management Systems (LMS).  
The system analyzes behavioral learning patterns using machine learning, explains predictions with interpretable AI, and generates actionable intervention guidance for educators.

---

## Landing Page

<p align="center">
  <img src="Landingpage.png" width="800">
</p>

---

## Overview

Students rarely drop out abruptly. Before disengagement occurs, they typically show measurable behavioral signals such as reduced engagement, delayed submissions, declining performance, and inconsistent learning activity.

This system analyzes behavioral patterns from LMS data and predicts dropout risk using a trained machine learning model. Explainable AI techniques highlight the key factors behind each prediction, while generative AI provides clear intervention guidance for educators.

The goal is to enable early intervention and support student success while keeping educators in control of decision-making.

---

## Goal

Enable early detection of disengagement patterns, provide explainable AI insights, and support timely educator interventions to reduce student dropout risk in digital learning environments.

---

## System Architecture
Learning Management System (LMS)
│
▼
Data Processing Layer
(Feature Engineering & Behavioral Signals)
│
▼
AI Intelligence Layer
(XGBoost Prediction + SHAP Explainability)
│
▼
Insight & Intervention Layer
(GenAI Recommendations + Alerts + Dashboard)

---

## Core Components

### API Layer
Handles secure ingestion of behavioral learning data and prediction requests.

### Cloud Storage
Stores datasets, trained models, and application assets.

### Machine Learning Model
An **XGBoost model** trained on behavioral engagement patterns to estimate dropout probability.

### Explainability Layer
**SHAP analysis** highlights the most influential behavioral factors behind predictions.

### AI Intervention Engine
Generative AI generates actionable recommendations to help educators support at-risk students.

### Dashboard & Alerts
Provides real-time risk analysis and automated notifications for high-risk students.

---

## Key Inputs

- Engagement signals such as login frequency, inactivity duration, and session activity  
- Learning interaction data including content completion, replays, and navigation behavior  
- Assessment performance metrics such as concept accuracy and failure patterns  
- Temporal engagement trends indicating declining participation over time  

---

## Outputs

### Students

- Engagement insights and behavioral awareness  
- Personalized guidance for improving learning consistency  

### Educators

- Dropout risk level (**Low / Moderate / High**)  
- Key behavioral drivers influencing risk predictions  
- AI-generated intervention recommendations  

---

## Technology Stack

- **Python & FastAPI** – Backend API and model inference  
- **Amazon S3** – Dataset storage, model artifacts, and frontend hosting  
- **Amazon SageMaker** – Machine learning model training  
- **AWS App Runner** – Scalable backend deployment  
- **Amazon Cognito** – Secure authentication and access control  
- **Amazon Bedrock** – Generative AI-based intervention recommendations  
- **Amazon SNS** – Automated alerts for high-risk students  
- **SHAP** – Explainable AI and model interpretability  

---

## Impact

The system transforms raw learning behavior data into actionable insights, enabling early intervention and improving student engagement and retention.

By combining **predictive analytics, explainable AI, and generative AI** on scalable cloud infrastructure, the solution demonstrates how intelligent systems can enhance modern digital education platforms.
