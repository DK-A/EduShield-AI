from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# ==============================
# 📦 Database
# ==============================
from database.db import engine
from database.models import Base

# ==============================
# 📦 Routers
# ==============================
from routers.email import router as email_router
from routers.oauth import router as oauth_router
from routers.gmail import router as gmail_router
from routers.security import router as security_router
from routers.dashboard import router as dashboard_router

# ==============================
# 🔥 CREATE DATABASE TABLES
# ==============================
Base.metadata.create_all(bind=engine)

# ==============================
# 🚀 Initialize FastAPI App
# ==============================
app = FastAPI(
    title="EduShield AI",
    version="1.0.0"
)

# ===================================================
# 🔐 CRITICAL: SESSION MIDDLEWARE MUST BE FIRST
# ===================================================
app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_TO_RANDOM_LONG_SECRET_123456789"
)

# ===================================================
# 🌍 CORS Middleware (AFTER SESSION)
# ===================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # safer than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 📦 Include Routers
# ==============================
app.include_router(email_router)
app.include_router(oauth_router)
app.include_router(gmail_router)
app.include_router(security_router)
app.include_router(dashboard_router)

# ==============================
# 🏠 Root Endpoint
# ==============================
@app.get("/")
def home():
    return {
        "message": "EduShield AI running 🚀",
        "dashboard": "Visit /dashboard",
        "features": [
            "Google OAuth Login",
            "Gmail Email Fetch",
            "Phishing Detection (ML + SHAP)",
            "Login Anomaly Detection",
            "Security Score Engine",
            "Database Logging",
            "Professional Dashboard"
        ]
    }