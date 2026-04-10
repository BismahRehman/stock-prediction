from fastapi import Depends, Response
from fastapi.security import HTTPAuthorizationCredentials

from app.dependency import get_db, get_current_user, security
from app.schema.user import RegisterRequest, LoginRequest
from app.repository.user import loginuser, createuser, logout_user
from fastapi import APIRouter
from app.model.Blacklist_Table import BlacklistedToken




router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login(user: LoginRequest, db=Depends(get_db)):

    user = await loginuser(user, db)
    return user



@router.post("/register")
async def register(user: RegisterRequest, db=Depends(get_db)  ):

    await createuser(user, db)
    return {"message": "User registered successfully"}



@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    await logout_user(credentials, db)

    return {"message": "Logged out successfully"}