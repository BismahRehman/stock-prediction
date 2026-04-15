# async def prediction_result(current_user,accuracy_results,model, db):
#
#     result = await  db.execute(select(User).where(User.email==current_user))
#     user = result.scalar_one_or_none()
#
#     prediction_history = PredictionHistory(user_id=user.id,model_name=model,accuracy=accuracy_results)
#     db.add(prediction_history)
#     await db.commit()
#     await db.refresh(prediction_history)
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.repository.prediction import prediction_result


@pytest.mark.asyncio
async def test_prediction_success():
    # --- Mock user ---
    mock_user= MagicMock()
    mock_user.email = "test@example.com"

    current_user = "test@example.com"
    accuracy_results = 0.92
    model = "model_v1"




    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    await prediction_result(current_user, accuracy_results, model, db=mock_db)

    # --- Assertions ---

    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


