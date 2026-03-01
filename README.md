# EduShield

**AI-Powered Email Threat Intelligence & Security Posture Platform**

EduShield is a privacy-first email threat intelligence system that analyzes inbox activity, computes real-time safety scores, categorizes threat levels, and visualizes overall security posture through an enterprise-style SOC dashboard.

The platform is designed for scalable backend deployment and future edge execution using the AMD Kria KV260 Vision AI Kit.

---

## Overview

EduShield bridges traditional spam filtering and modern security intelligence by combining:

- Machine learning–based phishing detection  
- Real-time inbox safety scoring  
- Risk categorization engine  
- Security posture computation  
- Explainable AI reasoning  
- Metadata-only privacy architecture  
- Edge deployment readiness  

---

## MVP Capabilities

### Email Safety Scoring
- ML-generated score between 0–100  
- 0 → Highly Dangerous  
- 100 → Fully Safe  

### Risk Categorization

| Score Range | Risk Level |
|------------|------------|
| 0 – 49     | High       |
| 50 – 74    | Medium     |
| 75 – 100   | Low        |

```python
if score < 50:
    risk = "High"
elif score < 75:
    risk = "Medium"
else:
    risk = "Low"
```

### Security Posture Score

```
Security Score = Average Safety Score (Latest 5 Emails)
```

Provides a real-time quantitative inbox health indicator.

---

## System Architecture (MVP)

```
Gmail API
   ↓
Phishing Model (Vectorizer + Classifier)
   ↓
Risk Mapping
   ↓
PostgreSQL (Metadata Storage Only)
   ↓
Security Score Engine
   ↓
FastAPI Backend
   ↓
SOC Dashboard Interface
```

---

## Edge Deployment Vision

EduShield is being architected for edge execution using:

**AMD Kria KV260 Vision AI Kit**

Planned edge capabilities:

- Lightweight inference engine
- ARM-based model optimization
- Reduced cloud dependency
- Privacy-preserving local processing
- Edge SOC-style monitoring interface

This enables scalable deployment in enterprise and secure network environments.

---

## Tech Stack

### Backend
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Python 3.12  

### Machine Learning
- Scikit-learn  
- TF-IDF Vectorizer  
- Serialized Phishing Model (.pkl)  

### Frontend
- HTML / CSS  
- JavaScript  
- Chart.js  

### Edge (Planned)
- AMD Kria KV260 Vision AI Kit  

---

## Current Project Structure

```
backend/

database/
├── db.py
├── models.py
└── __init__.py

model/
├── phishing_model.pkl
└── vectorizer.pkl

routers/
├── dashboard.py
├── email.py
├── gmail.py
├── login.py
├── oauth.py
├── score.py
├── security.py
└── __init__.py

services/
├── anomaly_service.py
├── auto_scan_service.py
├── gmail_service.py
├── login_service.py
├── phishing_service.py
├── scoring_service.py
└── security_service.py
```

---

## Privacy Design

EduShield follows strict privacy-first principles:

- No raw email body retention  
- Metadata-only database storage  
- No PII visualization in dashboard  
- Dynamic risk calculation independent of stored labels  
- Modular ML separation from UI layer  

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/edushield.git
cd edushield/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

```sql
CREATE DATABASE edushield;
```

Update `database/db.py`:

```python
DATABASE_URL = "postgresql://username:password@localhost/edushield"
```

Create tables:

```bash
python
>>> from database.db import Base, engine
>>> Base.metadata.create_all(bind=engine)
```

### 5. Run Server

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Dashboard:

```
http://127.0.0.1:8000/dashboard/your_email_here
```

---

## Roadmap

- XGBoost phishing classifier integration  
- SHAP explainability visualization  
- Isolation Forest login anomaly detection  
- JWT-based authentication system  
- Consent logging framework  
- Dockerized deployment  
- Edge inference demo on AMD Kria KV260  
- Alert notification engine  
- SOC severity gauge visualization  

---

## Disclaimer

EduShield is a cybersecurity innovation prototype intended for research and demonstration purposes.  
Enterprise-grade deployment requires additional security, compliance, and scalability enhancements.
