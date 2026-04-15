#
# async def user_history(db,email):
#
#     result = await db.execute(select(User).where(User.email == email))
#     user = result.scalar_one_or_none()
#
#
#     stmt = select(PredictionHistory).where(PredictionHistory.user_id == user.id)
#     result = await db.execute(stmt)
#     data = result.scalars().all()
#     return data
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.repository.history import user_history


@pytest.mark.asyncio
async def test_history_success():
    # --- mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"

    # --- Mock DB result ---
    # --- mock history data ---
    mock_history = [MagicMock(), MagicMock()]

    # --- first query (user) ---
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user

    # --- second query (history) ---
    mock_history_result = MagicMock()
    mock_history_result.scalars.return_value.all.return_value = mock_history


    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(side_effect=[mock_user_result, mock_history_result])
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    result = await user_history(email="user@example.com", db=mock_db)

    # --- Assertions ---
    assert result == mock_history
    mock_db.execute.assert_awaited()





