import stripe
from fastapi import HTTPException
from app.config import settings
from app.repository.stripe import handle_checkout_session


# -----------------------------------------
# Stripe configuration validation
# -----------------------------------------
if not settings.STRIPE_SECRET_KEY:
    raise Exception("Stripe keys not set in .env")

stripe.api_key = settings.STRIPE_SECRET_KEY


# -----------------------------------------
# CREATE SUBSCRIPTION CHECKOUT SESSION
# -----------------------------------------
async def subscription_checkout(current_user):

    try:
        # Find existing Stripe customer
        customers = await stripe.Customer.list_async(
            email=current_user,
            limit=1
        )

        if customers.data:
            customer = customers.data[0]
        else:
            customer = await stripe.Customer.create_async(
                email=current_user
            )

        # Create checkout session
        session = await stripe.checkout.Session.create_async(
            customer=customer.id,
            payment_method_types=['card'],
            line_items=[{
                'price': settings.PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{settings.DOMAIN_URL}/success?session_id=CHECKOUT_SESSION_ID",
            cancel_url=f"{settings.DOMAIN_URL}/cancel",
        )

        return session.url

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------------------
# STRIPE WEBHOOK HANDLER
# -----------------------------------------
async def webhook(request, db):

    # Read raw payload
    payload = await request.body()

    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Signature")

    # Handle successful checkout
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        await handle_checkout_session(session, db)