import httpx
from datetime import datetime, timedelta
from jose import jwt

from app.config import settings
from app.repository.google_auth import add_user


# -----------------------------------------
# STEP 1: Generate Google OAuth URL
# -----------------------------------------
async def login_google():

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    return google_auth_url


# -----------------------------------------
# STEP 2: OAuth callback handler
# -----------------------------------------
async def google_callback(code, db):

    # Exchange authorization code for access token
    data = {
        "code": code,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    # Call Google token endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.TOKEN_URL, data=data)
        token_response = response.json()

        access_token = token_response.get("access_token")

        # Fail-safe if token missing
        if not access_token:
            return {
                "error": "Failed to obtain access token",
                "details": token_response
            }

        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch user profile from Google
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                settings.USERINFO_URL,
                headers=headers
            )
            userinfo = userinfo_response.json()

    # Extract identity
    email = userinfo.get("email")

    # Create or fetch user in DB
    user = await add_user(db, email, userinfo)

    # -----------------------------------------
    # Generate internal JWT
    # -----------------------------------------
    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {
        "token_type": "bearer",
        "access_token": token
    }