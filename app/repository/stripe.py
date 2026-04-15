from sqlalchemy import select
from app.model.user import User
from datetime import datetime


# -----------------------------------------
# Stripe/Checkout webhook handler
# Upgrades user after successful payment
# -----------------------------------------
async def handle_checkout_session(session, db):

    # Extract email from checkout session
    customer_email = session.customer_details.email

    # Fetch user
    result = await db.execute(
        select(User).where(User.email == customer_email)
    )
    user = result.scalar_one_or_none()

    #
    user.subscription = "premium"
    user.token = user.token + 500
    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)