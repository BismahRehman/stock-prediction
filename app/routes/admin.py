
from fastapi import APIRouter, Depends
from app.dependency import get_db, get_admin
from app.repository.admin import banned_user, update_tokens, cancel_subscriptions, renew_subscriptions,unbanned_user

router = APIRouter(prefix="/admin", tags=["admin"])


# -----------------------------------
# BAN USER
# -----------------------------------
@router.post("/ban-user/{user_id}")
async def ban_user(
    user_id: int,
    admin=Depends(get_admin),
    db=Depends(get_db)
):
    await banned_user(user_id, db)
    return {"message": "User banned successfully"}


# -----------------------------------
# UNBAN USER
# -----------------------------------
@router.post("/unban-user/{user_id}")
async def unban_user(
    user_id: int,
    admin=Depends(get_admin),
    db=Depends(get_db)
):
    await unbanned_user(user_id, db)
    return {"message": "User unbanned successfully"}


# -----------------------------------
# RESET / UPDATE TOKENS
# -----------------------------------
@router.post("/update-tokens/{user_id}")
async def update_token(
    user_id: int,
    admin=Depends(get_admin),
    db=Depends(get_db)
):
    await update_tokens(user_id, db)
    return {"message": "User Token Update successfully"}


# -----------------------------------
# CANCEL SUBSCRIPTION
# -----------------------------------
@router.post("/cancel-subscription/{user_id}")
async def cancel_subscription(
    user_id: int,
    admin=Depends(get_admin),
    db=Depends(get_db)
):
    await cancel_subscriptions(user_id, db)
    return {"message": "User subscription Update successfully"}


# -----------------------------------
# RENEW SUBSCRIPTION
# -----------------------------------
@router.post("/renew-subscription/{user_id}")
async def renew_subscription(
    user_id: int,
    admin=Depends(get_admin),
    db=Depends(get_db)
):
    await renew_subscriptions(user_id, db)
    return {"message": "User subscription Update successfully"}