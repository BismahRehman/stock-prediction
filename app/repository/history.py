from fastapi import HTTPException
from app.model.user import User
from app.model.history import PredictionHistory
from sqlalchemy import select


# --------------------------------------
# Fetch prediction history of a user
# --------------------------------------
async def user_history(db, email):

    # Step 1: Resolve user by email
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    # Step 2: Validate user existence
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Step 3: Fetch related prediction history
    stmt = select(PredictionHistory).where(
        PredictionHistory.user_id == user.id
    )

    result = await db.execute(stmt)

    # Step 4: Extract all rows
    data = result.scalars().all()

    return data