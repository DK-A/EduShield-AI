from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import EmailScan
from datetime import datetime

user_tokens = {}

router = APIRouter(prefix="/gmail", tags=["Gmail"])


# ==============================
# Risk Mapping Based on Safety Score
# ==============================
def map_risk(score: float):
    if score < 50:
        return "High"
    elif score < 75:
        return "Medium"
    else:
        return "Low"


# ==============================
# AUTO SCAN (Demo Version)
# ==============================
@router.get("/auto-scan/{user_email}")
def auto_scan(user_email: str, db: Session = Depends(get_db)):

    print(f"🔥 AUTO SCAN STARTED FOR: {user_email}")

    # Clear old records (keep only fresh 5 for MVP)
    db.query(EmailScan).filter(
        EmailScan.user_email == user_email
    ).delete()

    # Demo Safety Scores (HIGH score = SAFE)
    demo_scores = [
        ("Security alert", 35),
        ("Boost your value now", 25),
        ("Session Reminder", 70),
        ("Welcome to Course", 92),
        ("Important Update", 85),
    ]

    for subject, score in demo_scores:

        risk_level = map_risk(score)

        scan_record = EmailScan(
            user_email=user_email,
            subject=subject,
            risk_score=score,   # THIS IS SAFETY SCORE
            risk_level=risk_level,
            created_at=datetime.utcnow()
        )

        db.add(scan_record)

    db.commit()

    print("✅ AUTO SCAN COMPLETED")

    return {"status": "scanned"}