from app.model.user import User
from app.model.history import PredictionHistory
from sqlalchemy import select



async def prediction_result(current_user,accuracy_results,model, db):

    result = await  db.execute(select(User).where(User.email==current_user))
    user = result.scalar_one_or_none()

    prediction_history = PredictionHistory(user_id=user.id,model_name=model,accuracy=accuracy_results)
    db.add(prediction_history)
    await db.commit()
    await db.refresh(prediction_history)
