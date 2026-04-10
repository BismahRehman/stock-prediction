

from fastapi import  HTTPException, status
from app.model.user import User
from datetime import datetime
from sqlalchemy import select



async def banned_user( user_id,db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.banned:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already banned")
    if  not user.banned:
        user.banned = True
    await db.commit()
    await db.refresh(user)



async def unbanned_user( user_id,db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not user.banned:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already unbanned")
    if  user.banned:
        user.banned = False
    await db.commit()
    await db.refresh(user)


async def update_tokens( user_id,db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    user.token = 100
    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)



async def cancel_subscriptions( user_id,db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.subscription == "free":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User already in free tier subscription ")

    user.subscription = "free"
    user.token = user.token - 500
    if user.token <0:
        user.token = 0
    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)


async def renew_subscriptions(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.subscription == "premium":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already in premium tier subscription ")

    user.subscription = "premium"
    user.token = user.token + 500
    user.last_reset_date =datetime.utcnow()

    await db.commit()
    await db.refresh(user)
