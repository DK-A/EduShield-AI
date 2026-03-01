from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from database.db import get_db
from database.models import LoginEvent, EmailScan
from services.anomaly_service import analyze_login

router = APIRouter(
    prefix="/login",
    tags=["Login Security"]
)

# ==========================================
# Request Model
# ==========================================

class LoginRequest(BaseModel):
    user_email: str
    hour: int
    device_known: int
    location_match: int


# ==========================================
# Verify Login Endpoint
# ==========================================

@router.post("/verify")
def verify_login(data: LoginRequest, db: Session = Depends(get_db)):

    result = analyze_login(
        hour=data.hour,
        device_known=data.device_known,
        location_match=data.location_match
    )

    anomaly_score = 0.9 if result["risk"] == "High" else 0.1

    login_event = LoginEvent(
        user_email=data.user_email,
        hour=data.hour,
        device_known=data.device_known,
        location_match=data.location_match,
        anomaly_score=anomaly_score,
        created_at=datetime.utcnow()
    )

    db.add(login_event)
    db.commit()

    return {
        "user_email": data.user_email,
        "risk_level": result["risk"],
        "anomaly_score": anomaly_score,
        "message": result["message"]
    }


# ==========================================
# ADVANCED UNIFIED SECURITY DASHBOARD API
# ==========================================

@router.get("/advanced-dashboard/{user_email}")
def advanced_dashboard(user_email: str, db: Session = Depends(get_db)):

    # ================= EMAIL ANALYSIS =================

    total_emails = db.query(EmailScan)\
        .filter(EmailScan.user_email == user_email)\
        .count()

    high_emails = db.query(EmailScan)\
        .filter(
            EmailScan.user_email == user_email,
            EmailScan.risk_level == "High"
        ).count()

    medium_emails = db.query(EmailScan)\
        .filter(
            EmailScan.user_email == user_email,
            EmailScan.risk_level == "Medium"
        ).count()

    low_emails = db.query(EmailScan)\
        .filter(
            EmailScan.user_email == user_email,
            EmailScan.risk_level == "Low"
        ).count()

    email_avg = db.query(func.avg(EmailScan.risk_score))\
        .filter(EmailScan.user_email == user_email)\
        .scalar() or 0


    # ================= LOGIN ANALYSIS =================

    total_logins = db.query(LoginEvent)\
        .filter(LoginEvent.user_email == user_email)\
        .count()

    high_logins = db.query(LoginEvent)\
        .filter(
            LoginEvent.user_email == user_email,
            LoginEvent.anomaly_score >= 0.8
        ).count()

    login_avg = db.query(func.avg(LoginEvent.anomaly_score))\
        .filter(LoginEvent.user_email == user_email)\
        .scalar() or 0

    login_scaled = login_avg * 100


    # ================= SECURITY FORMULA =================

    final_risk = (
        (email_avg * 0.6)
        + (login_scaled * 0.4)
        + (high_emails * 5)
        + (high_logins * 10)
    )

    security_score = max(100 - final_risk, 0)

    # ================= SECURITY LEVEL =================

    if security_score >= 80:
        level = "Secure"
    elif security_score >= 50:
        level = "Moderate"
    else:
        level = "High Risk"


    # ================= RISK TREND (Last 7 Days) =================

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    trend_query = db.query(
        func.date(EmailScan.created_at),
        func.avg(EmailScan.risk_score)
    ).filter(
        EmailScan.user_email == user_email,
        EmailScan.created_at >= seven_days_ago
    ).group_by(
        func.date(EmailScan.created_at)
    ).all()

    trend = [
        {"date": str(row[0]), "avg_score": round(float(row[1]), 2)}
        for row in trend_query
    ]


    # ================= TOP RISKY SENDERS =================

    sender_query = db.query(
        EmailScan.sender,
        func.count(EmailScan.id)
    ).filter(
        EmailScan.user_email == user_email,
        EmailScan.risk_level == "High"
    ).group_by(EmailScan.sender).all()

    top_senders = [
        {"sender": row[0], "count": row[1]}
        for row in sender_query
    ]


    return {
        "user_email": user_email,

        # Email stats
        "total_emails": total_emails,
        "high_emails": high_emails,
        "medium_emails": medium_emails,
        "low_emails": low_emails,

        # Login stats
        "total_logins": total_logins,
        "high_logins": high_logins,

        # Scores
        "email_risk_avg": round(email_avg, 2),
        "login_risk_avg": round(login_scaled, 2),
        "final_risk": round(final_risk, 2),
        "security_score": round(security_score, 2),
        "security_level": level,

        # Analytics
        "trend": trend,
        "top_senders": top_senders
    }