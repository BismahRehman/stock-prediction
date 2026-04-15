import pytest
from unittest.mock import MagicMock, AsyncMock

from app.repository.history import user_history


# =========================================================
# ================= SUCCESS CASE ===========================
# =========================================================

@pytest.mark.asyncio
async def test_user_history_success():
    """
    User exists → should return prediction history list
    """

    # --- Mock user ---
    mock_user = MagicMock(id=1, email="test@example.com")

    # --- Mock history ---
    mock_history = [MagicMock(), MagicMock()]

    # --- First query (user) ---
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user

    # --- Second query (history) ---
    mock_history_result = MagicMock()
    mock_history_result.scalars.return_value.all.return_value = mock_history

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(
        side_effect=[mock_user_result, mock_history_result]
    )

    # --- Call ---
    result = await user_history(email="test@example.com", db=mock_db)

    # --- Assertions ---
    assert result == mock_history

    # Ensure both queries were executed
    assert mock_db.execute.await_count == 2


# =========================================================
# ================= USER NOT FOUND =========================
# =========================================================

@pytest.mark.asyncio
async def test_user_history_user_not_found():
    """
    If user does not exist → should fail (current behavior: crash)
    """

    # --- First query returns None ---
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = None

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_user_result)

    # --- Call + Assert ---
    with pytest.raises(AttributeError):
        await user_history(email="test@example.com", db=mock_db)