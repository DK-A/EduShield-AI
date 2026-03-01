from sqlalchemy.orm import Session
from database.models import EmailScan, LoginEvent
from sqlalchemy import func

def calculate_security_score(user_email: str, db: Session):
    """
    Combines email phishing risk and login anomaly risk
    into a single security score (0–100).
    """

    # ===============================
    # Get Email Risk Average
    # ===============================
    email_avg = db.query(func.avg(EmailScan.risk_score))\
        .filter(EmailScan.user_email == user_email)\
        .scalar()

    if email_avg is None:
        email_avg = 0

    # ===============================
    # Get Login Anomaly Average
    # ===============================
    login_avg = db.query(func.avg(LoginEvent.anomaly_score))\
        .filter(LoginEvent.user_email == user_email)\
        .scalar()

    if login_avg is None:
        login_avg = 0

    # ===============================
    # Convert anomaly_score (0–1) to 0–100
    # ===============================
    login_avg_scaled = login_avg * 100

    # ===============================
    # Weighted Risk Formula
    # ===============================
    final_risk = (email_avg * 0.6) + (login_avg_scaled * 0.4)

    security_score = max(100 - final_risk, 0)

    return {
        "user_email": user_email,
        "email_risk_avg": round(email_avg, 2),
        "login_risk_avg": round(login_avg_scaled, 2),
        "final_risk": round(final_risk, 2),
        "security_score": round(security_score, 2)
    }