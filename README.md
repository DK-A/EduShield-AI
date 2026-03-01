# 🛡 EduShield

![Overview](assets/overview_edushield.png)

**AI-Powered Email Threat Intelligence & Security Posture Platform**

EduShield is a privacy-first email threat intelligence system that analyzes inbox activity, computes real-time safety scores, categorizes threat levels, and visualizes overall security posture through an enterprise-style SOC dashboard.

The platform is designed for scalable backend deployment and future edge execution using the AMD Kria KV260 Vision AI Kit.

---

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Status](https://img.shields.io/badge/Status-MVP-orange)

---

## 🚀 Overview

EduShield bridges traditional spam filtering and modern security intelligence by combining:

- Machine learning–based phishing detection  
- Real-time inbox safety scoring  
- Risk categorization engine  
- Security posture computation  
- Explainable AI reasoning  
- Metadata-only privacy architecture  
- Edge deployment readiness  

---

## 🏗 System Architecture

![Architecture](assets/architecture.jpeg)

### Processing Flow

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

## 🎥 MVP Demo Video

Watch the full EduShield MVP demo here:

👉 **[Click to Watch Demo](PASTE_YOUR_GOOGLE_DRIVE_LINK_HERE)**  
*(Set Drive access to “Anyone with the link → Viewer”)*

---

## 🧠 MVP Capabilities

### 1️⃣ Email Safety Scoring

- ML-generated score between **0–100**  
- 0 → Highly Dangerous  
- 100 → Fully Safe  

```python
if score < 50:
    risk = "High"
elif score < 75:
    risk = "Medium"
else:
    risk = "Low"
```

---

### 2️⃣ Risk Categorization

| Score Range | Risk Level |
|------------|------------|
| 0 – 49     | High       |
| 50 – 74    | Medium     |
| 75 – 100   | Low        |

---

### 3️⃣ Security Posture Score

```
Security Score = Average Safety Score (Latest 5 Emails)
```

Provides a real-time quantitative inbox health indicator.

---

## 🔐 Privacy-First Design

EduShield follows strict privacy principles:

- No raw email body retention  
- Metadata-only database storage  
- No PII visualization in dashboard  
- Dynamic risk calculation independent of stored labels  
- Modular ML separation from UI layer  

---

## ⚙ Tech Stack

### Backend
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Python 3.12  

### Machine Learning
- Scikit-learn  
- TF-IDF Vectorizer  
- Serialized Phishing Model  

### Frontend
- HTML / CSS  
- JavaScript  
- Chart.js  

### Edge (Planned)
- AMD Kria KV260 Vision AI Kit  

---

## 📂 Project Structure

```
EduShield-AI
│
├── backend/
│   ├── database/
│   ├── routers/
│   ├── services/
│   ├── main.py
│   └── requirements.txt
│
├── assets/
│   ├── overview_edushield.png
│   └── architecture.jpeg
│
├── README.md
└── .gitignore
```

---

## 🖥 Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/DK-A/EduShield-AI.git
cd EduShield-AI/backend
```

---

### 2️⃣ Create Virtual Environment

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

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure PostgreSQL

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

---

### 5️⃣ Run Server

```bash
uvicorn main:app --reload
```

Server:
```
http://127.0.0.1:8000
```

Dashboard:
```
http://127.0.0.1:8000/dashboard/your_email_here
```

---

## 🛣 Roadmap

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

## ⚠ Disclaimer

EduShield is a cybersecurity innovation prototype intended for research and demonstration purposes.  
Enterprise-grade deployment requires additional security, compliance, and scalability enhancements.
