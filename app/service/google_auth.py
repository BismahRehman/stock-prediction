import datetime
from datetime import datetime, timedelta

import httpx
# import requests

from jose import jwt
from app.config import settings
from app.repository.google_auth import add_user



async def login_google():
    # Redirect user to Google login
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

async def google_callback(code, db ):
    # Exchange code for token
    data = {
        "code": code,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(settings.TOKEN_URL, data=data)
        token_response = response.json()
        access_token = token_response.get("access_token")

        if not access_token:
            return {"error": "Failed to obtain access token", "details": token_response}

        header = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(settings.USERINFO_URL, headers=header)
            userinfo = userinfo_response.json()


    if not  userinfo.get("email"):
         return {"error": "Email not found", "details": userinfo}

    email = userinfo.get("email")
    user =  await add_user(db, email, userinfo)

    #  Generate Jwt token
    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return { "token_type": "bearer","access_token": token}

