# LMS-Early-Dropout-Risk-Engine
An AI-powered early warning system that integrates with existing Learning Management Systems (LMS) to detect early signs of student disengagement and predict dropout risk using behavioral and performance data.

##1.Overview

Students rarely drop out suddenly.
Before disengaging, they show measurable patterns such as reduced activity, declining performance, and prolonged inactivity.

This system passively observes LMS events, analyzes trends using a pre-trained machine learning model, and generates explainable insights for students and educators.

AI supports decisions — teachers remain in control.

##2.System Architecture
LMS Platform
      ↓ (raw events)
Data Collection Layer
      ↓ (feature engineering)
AI Intelligence Layer
      ↓ (risk prediction + explainability)
Reporting & Feedback Layer

##3.Core Components

API Layer – Secure data ingestion

Cloud Storage (S3 / RDS) – Event & profile storage

ML Model (SageMaker / Python) – Risk prediction

Explainability (SHAP) – Contributing factors

Dashboard & Alerts – Student and teacher insights

##4.AI Design Principles

Pre-trained global model

Per-student feature tracking

Time-windowed behavioral modeling

Periodic retraining (not per interaction)

Explainable predictions (no black-box decisions)

##5.Key Inputs

Engagement metrics (session duration, inactivity, login frequency)

Learning interaction data (video completion, replays)

Assessment performance (topic accuracy, error patterns)

Temporal trends (week-to-week engagement decay)

##6.Outputs

Students

Focus & engagement score

Personalized improvement insights

Teachers

Dropout risk level (Low / Medium / High)

Top contributing risk factors

Engagement trend analysis

##Tech Stack

Python • AWS (API Gateway, S3, RDS, SageMaker) • SHAP

##Goal

Enable early detection, empower students through self-awareness, and support teacher-led interventions to reduce dropout risk.
