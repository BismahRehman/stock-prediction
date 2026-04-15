import pytest
from unittest.mock import MagicMock, AsyncMock

from app.repository.prediction import prediction_result


# =========================================================
# ================= SUCCESS CASE ===========================
# =========================================================

@pytest.mark.asyncio
async def test_prediction_result_success():
    """
    Should create prediction history and save to DB
    """

    # --- Mock user ---
    mock_user = MagicMock(id=1, email="test@example.com")

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

    # --- Call ---
    await prediction_result(current_user, accuracy_results, model, db=mock_db)

    # --- Assertions ---
    mock_db.add.assert_called_once()

    created_obj = mock_db.add.call_args[0][0]

    assert created_obj.user_id == 1
    assert created_obj.model_name == model
    assert created_obj.accuracy == accuracy_results

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(created_obj)


# =========================================================
# ================= USER NOT FOUND =========================
# =========================================================

@pytest.mark.asyncio
async def test_prediction_result_user_not_found():
    """
    If user does not exist → current behavior = crash
    """

    # --- DB returns None ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    # --- Expect failure ---
    with pytest.raises(AttributeError):
        await prediction_result(
            current_user="test@example.com",
            accuracy_results=0.92,
            model="model_v1",
            db=mock_db
        )