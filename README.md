# LMS Early Dropout Risk Engine

An AI-powered early warning system that integrates with Learning Management Systems (LMS) to detect early signs of student disengagement and predict dropout risk using behavioral learning data. The system combines machine learning, explainable AI, and generative AI to provide actionable insights for educators and students.

## Overview

Students rarely drop out abruptly. Before disengagement occurs, they typically show measurable behavioral signals such as reduced engagement, delayed submissions, declining performance, and inconsistent learning activity.

This system analyzes behavioral patterns from LMS data and predicts dropout risk using a trained machine learning model. Explainable AI techniques highlight the key factors behind each prediction, while generative AI provides clear intervention guidance for educators.

The goal is to enable early intervention and support student success while keeping educators in control of decision-making.

## Goal

Enable early detection of disengagement patterns, provide explainable AI insights, and support timely educator interventions to reduce student dropout risk in digital learning environments.

## System Architecture

LMS Platform
↓ (student activity and learning events)
Data Processing Layer
↓ (feature engineering and behavioral signals)
AI Intelligence Layer
↓ (risk prediction and explainability)
Insight & Intervention Layer

## Core Components

API Layer
Handles secure ingestion of behavioral learning data and prediction requests.

Cloud Storage
Stores datasets, trained models, and application assets.

Machine Learning Model
An XGBoost model trained on behavioral engagement patterns to estimate dropout probability.

Explainability Layer
SHAP analysis highlights the most influential behavioral factors behind predictions.

AI Intervention Engine
Generative AI generates actionable recommendations to help educators support at-risk students.

Dashboard and Alerts
Provides real-time risk analysis and automated notifications for high-risk students.

## Key Inputs

Engagement signals such as login frequency, inactivity duration, and session activity.

Learning interaction data including content completion, replays, and navigation behavior.

Assessment performance metrics such as concept accuracy and failure patterns.

Temporal engagement trends indicating declining participation over time.

## Outputs

## Students

Engagement insights and behavioral awareness.

Personalized guidance for improving learning consistency.

## Educators

Dropout risk levels categorized as Low, Moderate, or High.

Key behavioral drivers influencing risk predictions.

AI-generated intervention recommendations.

## Technology Stack

Python and FastAPI for backend services.

AWS S3 for dataset storage, model artifacts, and frontend hosting.

Amazon SageMaker for machine learning model training.

AWS App Runner for scalable backend deployment.

Amazon Cognito for secure user authentication and access control.

Amazon Bedrock for generative AI-based intervention recommendations.

Amazon SNS for automated alerts and notifications.

SHAP for explainable AI and model interpretability.

## Impact

The system transforms raw learning behavior data into actionable insights, enabling early intervention and improving student engagement and retention.

By combining predictive analytics, explainable AI, and generative AI on scalable cloud infrastructure, the solution demonstrates how intelligent systems can enhance modern digital education platforms.
