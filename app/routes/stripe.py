
import stripe
from fastapi import APIRouter, Request, Depends

from app.dependency import get_current_user, get_db
from app.config import settings
from app.service.stripe import subscription_checkout,webhook


if not settings.STRIPE_SECRET_KEY :
    raise Exception("Stripe keys not set in .env")

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(tags=["Stripe"])


# =================== This is used for subscription management ===================



@router.post("/create-subscription-checkout")
async def create_subscription_checkout(current_user: str = Depends(get_current_user)):

    session_url= await subscription_checkout(current_user)

    return {"session": session_url}






@router.post("/webhook")
async def stripe_webhook(request: Request, db= Depends(get_db)):

    await (webhook(request, db))

    return {"status": "success"}


@router.get("/success")
async def success_page():

    return {"message": "Payment Successful! Thank you for your purchase."}

@router.get("/cancel")
def cancel_page():

    return {"message": "Payment was cancelled."}




