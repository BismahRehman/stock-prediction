from fastapi import HTTPException, status
from app.model.user import User
from datetime import datetime
from sqlalchemy import select


# ----------------------------
# Ban a user
# ----------------------------
async def banned_user(user_id, db):
    # Fetch user from DB
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    # Validate user existence
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent redundant operation
    if user.banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already banned"
        )

    # Mark user as banned
    user.banned = True

    # Persist changes
    await db.commit()
    await db.refresh(user)


# ----------------------------
# Unban a user
# ----------------------------
async def unbanned_user(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent redundant operation
    if not user.banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already unbanned"
        )

    # Restore user access
    user.banned = False

    await db.commit()
    await db.refresh(user)


# ----------------------------
# Reset user tokens (admin action)
# ----------------------------
async def update_tokens(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Reset token quota
    user.token = 100

    # Track reset time for audit / billing logic
    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)


# ----------------------------
# Cancel subscription (downgrade to free)
# ----------------------------
async def cancel_subscriptions(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Already at lowest tier
    if user.subscription == "free":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in free tier subscription"
        )

    # Downgrade subscription
    user.subscription = "free"

    # Deduct penalty / adjustment tokens
    user.token = user.token - 500

    # Prevent negative token state
    if user.token < 0:
        user.token = 0

    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)


# ----------------------------
# Renew subscription (upgrade to premium)
# ----------------------------
async def renew_subscriptions(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Already premium check
    if user.subscription == "premium":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already in premium tier subscription"
        )

    # Upgrade subscription
    user.subscription = "premium"

    # Reward tokens on upgrade
    user.token = user.token + 500

    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)