import stripe
from fastapi import APIRouter, Request, Depends

from app.dependency import get_current_user, get_db
from app.config import settings
from app.service.stripe import subscription_checkout, webhook

# -----------------------------------------
# Validate Stripe configuration at startup
# -----------------------------------------
if not settings.STRIPE_SECRET_KEY:
    raise Exception("Stripe keys not set in .env")

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(tags=["Stripe"])


# -----------------------------------------
# CREATE CHECKOUT SESSION
# -----------------------------------------
@router.get("/create-subscription-checkout")
async def create_subscription_checkout(
    current_user: str = Depends(get_current_user)
):

    session_url = await subscription_checkout(current_user)

    return {"session": session_url}


# -----------------------------------------
# STRIPE WEBHOOK (critical endpoint)
# -----------------------------------------
@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db=Depends(get_db)
):

    # Process Stripe event
    await webhook(request, db)

    return {"status": "success"}


# -----------------------------------------
# SUCCESS CALLBACK (UI redirect)
# -----------------------------------------
@router.get("/success")
async def success_page():
    return {"message": "Payment Successful! Thank you for your purchase."}


# -----------------------------------------
# CANCEL CALLBACK (UI redirect)
# -----------------------------------------
@router.get("/cancel")
def cancel_page():
    return {"message": "Payment was cancelled."}