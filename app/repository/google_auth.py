from app.model.user import User
from sqlalchemy import select


# ----------------------------------------
# Create user if not exists (Google OAuth)
# ----------------------------------------
async def add_user(db, email, userinfo):

    # Step 1: Check if user already exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    # Step 2: If user does not exist, create one
    if not user:
        user = User(
            email=email,
            google_id=userinfo.get("sub"),  # Google unique identifier (OAuth subject)
            auth_provider="google"
        )

        # Add to session
        db.add(user)

        # Persist to database
        await db.commit()

        # Refresh ORM object with DB-generated fields (id, timestamps, etc.)
        await db.refresh(user)

    # Step 3: Return existing or newly created user
    return user