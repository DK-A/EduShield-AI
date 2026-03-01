from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from database.db import get_db
from database.models import LoginEvent
from services.anomaly_service import analyze_login

router = APIRouter(
    prefix="/login",
    tags=["Login Security"]
)

# ================================
# Request Model
# ================================

class LoginRequest(BaseModel):
    user_email: str
    hour: int
    device_known: int
    location_match: int


# ================================
# Verify Login Endpoint
# ================================

@router.post("/verify")
def verify_login(data: LoginRequest, db: Session = Depends(get_db)):
    
    # Run ML anomaly detection
    result = analyze_login(
        hour=data.hour,
        device_known=data.device_known,
        location_match=data.location_match
    )

    # Convert risk to numeric score
    if result["risk"] == "High":
        risk_score = 90
    else:
        risk_score = 20

    # Store event in PostgreSQL
    login_event = LoginEvent(
        user_email=data.user_email,
        hour=data.hour,
        device_known=data.device_known,
        location_match=data.location_match,
        risk_level=result["risk"],
        risk_score=risk_score,
        timestamp=datetime.utcnow()
    )

    db.add(login_event)
    db.commit()

    return {
        "user_email": data.user_email,
        "risk_level": result["risk"],
        "risk_score": risk_score,
        "message": result["message"],
        "reason": result.get("reason", "Login appears normal")
    }