
from app.model.user import User
from sqlalchemy import select


async def add_user(db, email,userinfo):

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=email,
            google_id=userinfo.get("sub"),  # Google’s unique user ID
            auth_provider="google"

            # other fields as needed
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user