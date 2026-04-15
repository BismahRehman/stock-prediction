import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock

from app.repository.stripe import handle_checkout_session


# =========================================================
# ================= SUCCESS CASE ===========================
# =========================================================

@pytest.mark.asyncio
async def test_handle_checkout_session_success():
    """
    On successful checkout:
    - User upgraded to premium
    - Tokens increased
    - Timestamp updated
    """

    # --- Mock session ---
    mock_session = MagicMock()
    mock_session.customer_details.email = "test@gmail.com"

    # --- Mock user ---
    mock_user = MagicMock(
        id=1,
        email="test@gmail.com",
        token=100,
        subscription="free",
        last_reset_date=None
    )

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call ---
    await handle_checkout_session(mock_session, mock_db)

    # --- Assertions ---
    assert mock_user.subscription == "premium"
    assert mock_user.token == 600
    assert isinstance(mock_user.last_reset_date, datetime)

    # Ensure DB interaction
    mock_db.execute.assert_awaited_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)


# =========================================================
# ================= USER NOT FOUND =========================
# =========================================================

@pytest.mark.asyncio
async def test_handle_checkout_session_user_not_found():
    """
    If user does not exist → current behavior = crash
    """

    mock_session = MagicMock()
    mock_session.customer_details.email = "test@gmail.com"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(AttributeError):
        await handle_checkout_session(mock_session, mock_db)