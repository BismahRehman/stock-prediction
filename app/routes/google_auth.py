from fastapi import APIRouter, Depends
from app.dependency import get_db
from app.schema.user import LoginResponse, Google_URL, TokenResponse
from app.service.google_auth import login_google, google_callback

router = APIRouter(prefix="/auth/google", tags=["authentication"])


# -----------------------------------
# STEP 1: Redirect user to Google
# -----------------------------------
@router.get("/login")
async def login_with_google():

    # Generate Google OAuth URL
    google_auth_url = await login_google()

    return {"url": google_auth_url}


# -----------------------------------
# STEP 2: Google OAuth callback
# -----------------------------------
@router.get("/callback", response_model=TokenResponse)
async def callback(code: str, db=Depends(get_db)):

    # Exchange auth code for user + token
    token = await google_callback(code, db)

    return token