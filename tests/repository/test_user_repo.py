import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import HTTPException

from app.repository.user import loginuser


# =========================================================
# SUCCESS CASE
# =========================================================

@pytest.mark.asyncio
async def test_loginuser_success(monkeypatch):

    # --- input ---
    mock_user = MagicMock(email="test@gmail.com", password="plain")

    # --- db user ---
    db_user = MagicMock(
        email="test@gmail.com",
        hashed_password="hashed",
        banned=False
    )

    # --- DB mock ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = db_user

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    # --- external dependencies ---
    monkeypatch.setattr(
        "app.repository.user.verify_password",
        lambda a, b: True
    )

    monkeypatch.setattr(
        "app.repository.user.create_access_token",
        lambda data: "fake_token"
    )

    # --- call ---
    result = await loginuser(mock_user, mock_db)

    # --- assertions ---
    assert result["access_token"] == "fake_token"
    assert result["token_type"] == "bearer"


# =========================================================
# PASSWORD FAIL
# =========================================================

@pytest.mark.asyncio
async def test_loginuser_wrong_password(monkeypatch):

    mock_user = MagicMock(email="test@gmail.com", password="plain")

    db_user = MagicMock(
        email="test@gmail.com",
        hashed_password="hashed",
        banned=False
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = db_user

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    monkeypatch.setattr(
        "app.repository.user.verify_password",
        lambda a, b: False
    )

    with pytest.raises(HTTPException) as exc:
        await loginuser(mock_user, mock_db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect password for user"


# =========================================================
# USER NOT FOUND
# =========================================================

@pytest.mark.asyncio
async def test_loginuser_user_not_found(monkeypatch):

    mock_user = MagicMock(email="test@gmail.com", password="plain")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc:
        await loginuser(mock_user, mock_db)

    assert exc.value.status_code == 404