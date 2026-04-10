from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jose import JWTError
from starlette import status
from app.service.auth import verify_access_token
from app.database import AsyncSessionLocal as SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from  sqlalchemy import select
from app.model.user import User




async def get_db():
    async with SessionLocal() as db:
        yield db


# ============================== AUTH SECURITY ===========================================

security = HTTPBearer()


# ============================== CURRENT USER ============================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),db = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Send a Bearer token.",
        )

    token = credentials.credentials

    # 🔴 Check DB instead of set()
    result = await db.execute(
        select(BlacklistedToken).where(BlacklistedToken.token == token)
    )
    blacklisted = result.scalar_one_or_none()

    if blacklisted:
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = verify_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        useremail: str = payload.get("sub")
        if useremail is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return useremail

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def reset_tokens(user,db):
    now = datetime.utcnow()
    # reset if never reset or 30+ days passed
    if user.last_reset_date is None or now >= user.last_reset_date + timedelta(days=30):
        user.tokens_remaining = 100
        user.last_reset_date = now
        await  db.commit()
        await db.refresh(user)


async def get_token(user=Depends(get_current_user), db=Depends(get_db)):

    result = await db.execute(select(User).where(User.email == user))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")


    await reset_tokens(db_user, db)

    if int(db_user.token) < 10 :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return db_user.token



async def update_token(user, db, token):
    result = await db.execute(select(User).where(User.email == user))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.token = int(token) - 10

    await db.commit()
    await db.refresh(db_user)

    return db_user.token


async def get_admin(db=Depends(get_db), user=  Depends(get_current_user)):

    result = await db.execute(select(User).where(User.email == user))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    role = db_user.role
    if role != "admin":
        raise HTTPException(status_code=403, detail="Access Denied")
    return role




