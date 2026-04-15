import pytest
from unittest.mock import MagicMock, AsyncMock

from app.repository.google_auth import add_user


# =========================================================
# =============== USER DOES NOT EXIST ======================
# =========================================================

@pytest.mark.asyncio
async def test_add_user_creates_new_user():
    """
    If user does not exist:
    - New user should be created
    - DB add/commit/refresh should be called
    - Correct fields should be assigned
    """

    userinfo = {"sub": "google123"}
    email = "test@example.com"

    # DB returns None → user not found
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call ---
    user = await add_user(db=mock_db, email=email, userinfo=userinfo)

    # --- Assertions ---
    mock_db.add.assert_called_once()

    created_user = mock_db.add.call_args[0][0]

    assert created_user.email == email
    assert created_user.google_id == "google123"
    assert created_user.auth_provider == "google"

    assert user == created_user

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(created_user)


# =========================================================
# ================= USER ALREADY EXISTS ====================
# =========================================================

@pytest.mark.asyncio
async def test_add_user_returns_existing_user():
    """
    If user already exists:
    - Should NOT create new user
    - Should return existing user
    - No DB write operations
    """

    existing_user = MagicMock(email="test@example.com")

    userinfo = {"sub": "google123"}
    email = "test@example.com"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_user

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call ---
    user = await add_user(db=mock_db, email=email, userinfo=userinfo)

    # --- Assertions ---
    assert user == existing_user

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()