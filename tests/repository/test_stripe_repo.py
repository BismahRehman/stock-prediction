# async def handle_checkout_session(session, db):
#     """Called when checkout is completed"""
#     customer_email = session.customer_details.email
#     result = await db.execute(select(User).where(User.email == customer_email))
#
#     user = result.scalar_one_or_none()
#     user.subscription = "premium"
#     user.token = user.token + 500
#     user.last_reset_date = datetime.utcnow()
#
#     await db.commit()
#     await db.refresh(user)
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.repository.stripe import handle_checkout_session


@pytest.mark.asyncio
async def test_prediction_success():
    # --- Mock user ---
    mock_session = MagicMock()
    mock_session.customer_details.email = "test@gmail.com"

    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.email = "test@gmail.com"
    mock_user.token = 100
    mock_user.subscription = "free"
    mock_user.last_reset_date = None

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    await handle_checkout_session(mock_session, mock_db)

    # --- Assertions ---

    # --- Assertions ---
    assert mock_user.token == 600
    assert mock_user.subscription == "premium"
    assert isinstance(mock_user.last_reset_date, datetime)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)

