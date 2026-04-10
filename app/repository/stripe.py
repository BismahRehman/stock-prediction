from sqlalchemy import select
from app.model.user import User
from datetime import datetime


async def handle_checkout_session(session, db):
    """Called when checkout is completed"""
    customer_email = session.customer_details.email

    result = await db.execute(select(User).where(User.email == customer_email))

    user = result.scalar_one_or_none()
    user.subscription = "premium"
    user.token = user.token + 500
    user.last_reset_date = datetime.utcnow()

    await db.commit()
    await db.refresh(user)