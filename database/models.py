from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database.db import Base
from datetime import datetime


class EmailScan(Base):
    __tablename__ = "email_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    subject = Column(String)
    sender = Column(String)
    risk_score = Column(Float)
    risk_level = Column(String)

    # 🔥 Store SHAP explanation
    explanation = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class LoginEvent(Base):
    __tablename__ = "login_events"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    hour = Column(Integer)
    device_known = Column(Integer)
    location_match = Column(Integer)
    anomaly_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)