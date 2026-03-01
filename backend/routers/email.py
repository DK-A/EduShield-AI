from fastapi import APIRouter
from pydantic import BaseModel
from services.phishing_service import analyze_email

router = APIRouter()

class EmailRequest(BaseModel):
    content: str

@router.post("/scan-email")
def scan_email(email: EmailRequest):
    return analyze_email(email.content)