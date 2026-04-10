

from fastapi import HTTPException

from app.model.user import User
from app.model.history import PredictionHistory
from sqlalchemy import select



async def user_history(db,email):

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # results = await (db.query(PredictionHistory).filter(PredictionHistory.user_id == user.id).all())
    stmt = select(PredictionHistory).where(PredictionHistory.user_id == user.id)
    result = await db.execute(stmt)
    data = result.scalars().all()
    return data