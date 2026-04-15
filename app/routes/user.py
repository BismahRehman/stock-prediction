from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.dependency import get_db, security
from app.schema.user import RegisterRequest, LoginRequest
from app.repository.user import loginuser, createuser, logout_user

router = APIRouter(prefix="/auth", tags=["authentication"])


# -----------------------------------
# LOGIN
# -----------------------------------
@router.post("/login")
async def login(user: LoginRequest, db=Depends(get_db)):

    # Authenticate user + generate token
    return await loginuser(user, db)


# -----------------------------------
# REGISTER
# -----------------------------------
@router.post("/register")
async def register(user: RegisterRequest, db=Depends(get_db)):

    await createuser(user, db)
    return {"message": "User registered successfully"}


# -----------------------------------
# LOGOUT
# -----------------------------------
@router.get("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):

    await logout_user(credentials, db)
    return {"message": "Logged out successfully"}