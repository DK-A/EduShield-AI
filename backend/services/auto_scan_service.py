from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from sqlalchemy.orm import Session
import base64

from services.phishing_service import analyze_email
from database.models import EmailScan


def auto_scan_last_5(user_email: str, token_data: dict, db: Session):

    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scope")
    )

    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"),
            ""
        )

        sender = next(
            (h["value"] for h in headers if h["name"] == "From"),
            ""
        )

        body = ""

        if "parts" in msg_data["payload"]:
            for part in msg_data["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    if "data" in part["body"]:
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"]
                        ).decode("utf-8", errors="ignore")
        else:
            if "data" in msg_data["payload"]["body"]:
                body = base64.urlsafe_b64decode(
                    msg_data["payload"]["body"]["data"]
                ).decode("utf-8", errors="ignore")

        full_text = subject + " " + body

        # 🔥 FIX: Pass sender also (your model expects it)
        analysis = analyze_email(full_text, sender)

        # 🔥 Align with DB naming
        risk_score = analysis.get("final_risk_score", 0)
        risk_level = analysis.get("risk_level", "Low")

        email_scan = EmailScan(
            user_email=user_email,
            subject=subject,
            sender=sender,
            risk_score=risk_score,
            risk_level=risk_level
        )

        db.add(email_scan)

    db.commit()