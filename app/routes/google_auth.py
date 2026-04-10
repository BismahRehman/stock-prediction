from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from app.dependency import get_db
from app.schema.user import LoginResponse, Google_URL, TokenResponse

from app.service.google_auth import login_google, google_callback


router = APIRouter(prefix="/auth/google", tags=["authentication"])



@router.get("/login")
async def login_with_google():

    google_auth_url = await login_google()

    return {"url":google_auth_url}


@router.get("/callback", response_model=TokenResponse)
async def callback(code: str, db = Depends(get_db)):

    token =  await ( google_callback(code, db,))

    return token

