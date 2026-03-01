from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

from routers.gmail import user_tokens
from database.db import SessionLocal
from services.auto_scan_service import auto_scan_last_5


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth = OAuth()

# ---------------------------------------------------
# PURE OAUTH2 CONFIG (NO OPENID, NO METADATA)
# ---------------------------------------------------
oauth.register(
    name="google",
    client_id="xxxx",
    client_secret="xxxx",
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/",
    client_kwargs={
        # 🔥 No openid
        "scope": "email profile https://www.googleapis.com/auth/gmail.readonly",
        "access_type": "offline",
        "prompt": "consent",
    },
)

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


# ---------------------------------------------------
# CALLBACK + AUTO SCAN
# ---------------------------------------------------
@router.get("/callback")
async def auth_callback(request: Request):

    try:
        # Exchange authorization code for token
        token = await oauth.google.authorize_access_token(request)

        # Fetch user info manually (OAuth2 way)
        resp = await oauth.google.get(
            "oauth2/v2/userinfo",
            token=token
        )

        user = resp.json()
        email = user["email"]

        # Attach client info for Gmail API usage
        token["client_id"] = oauth.google.client_id
        token["client_secret"] = oauth.google.client_secret

        user_tokens[email] = token

        print("🔥 AUTO SCAN STARTED FOR:", email)

        db = SessionLocal()
        auto_scan_last_5(email, token, db)
        db.close()

        print("✅ AUTO SCAN COMPLETED")

        return RedirectResponse(url=f"/dashboard/{email}")

    except Exception as e:
        print("❌ OAUTH ERROR:", str(e))
        return {"error": str(e)}