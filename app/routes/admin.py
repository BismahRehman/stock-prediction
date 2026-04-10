
from fastapi import APIRouter, Depends
from app.dependency import get_db, get_admin
from app.repository.admin import banned_user, update_tokens, cancel_subscriptions, renew_subscriptions,unbanned_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/ban-user/{user_id}")
async def ban_user( user_id: int,  admin = Depends(get_admin),db=Depends(get_db)):
    await  banned_user(user_id, db)

    return {"message": "User banned successfully"}


@router.post("/unban-user/{user_id}")
async def unban_user( user_id: int,  admin = Depends(get_admin),db=Depends(get_db)):
    await unbanned_user(user_id, db)

    return {"message": "User unbanned successfully"}

@router.post("/update-tokens/{user_id}")
async def update_token( user_id: int,  admin = Depends(get_admin),db=Depends(get_db)):
    await update_tokens(user_id, db)

    return {"message": "User Token Update successfully"}




@router.post("/cancel-subscription/{user_id}")
async def cancel_subscription( user_id: int,  admin = Depends(get_admin),db=Depends(get_db)):
    await cancel_subscriptions(user_id, db)



    return {"message": "User subscription Update successfully"}


@router.post("/renew-subscription/{user_id}")
async def renew_subscription(user_id: int, admin=Depends(get_admin), db=Depends(get_db)):
    await  renew_subscriptions(user_id, db)


    return {"message": "User subscription Update successfully"}









