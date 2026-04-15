import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from app.repository.admin import (
    banned_user,
    unbanned_user,
    update_tokens,
    cancel_subscriptions,
    renew_subscriptions
)

# =========================================================
# Helper: Create Mock DB + Result
# =========================================================

def create_mock_db(user):
    """
    Creates a mocked async DB session with a given user.
    """
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    return mock_db


# =========================================================
# ===================== BANNED USER ========================
# =========================================================

@pytest.mark.asyncio
async def test_banned_user_success():
    """
    User exists and is not banned → should be banned successfully
    """
    user = MagicMock(id=1, banned=False)
    db = create_mock_db(user)

    await banned_user(user_id=1, db=db)

    assert user.banned is True
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_banned_user_not_found():
    """
    User does not exist → should raise 404
    """
    db = create_mock_db(None)

    with pytest.raises(HTTPException) as exc:
        await banned_user(user_id=1, db=db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


@pytest.mark.asyncio
async def test_banned_user_already_banned():
    """
    User already banned → should raise 400
    """
    user = MagicMock(id=1, banned=True)
    db = create_mock_db(user)

    with pytest.raises(HTTPException) as exc:
        await banned_user(user_id=1, db=db)

    assert exc.value.status_code == 400
    assert exc.value.detail == "User already banned"


# =========================================================
# ===================== UNBANNED USER ======================
# =========================================================

@pytest.mark.asyncio
async def test_unbanned_user_success():
    """
    User is banned → should be unbanned
    """
    user = MagicMock(id=1, banned=True)
    db = create_mock_db(user)

    await unbanned_user(user_id=1, db=db)

    assert user.banned is False
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_unbanned_user_not_found():
    """
    User not found → should raise 404
    """
    db = create_mock_db(None)

    with pytest.raises(HTTPException) as exc:
        await unbanned_user(user_id=1, db=db)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_unbanned_user_already_unbanned():
    """
    User already unbanned → should raise 400
    """
    user = MagicMock(id=1, banned=False)
    db = create_mock_db(user)

    with pytest.raises(HTTPException) as exc:
        await unbanned_user(user_id=1, db=db)

    assert exc.value.status_code == 400
    assert exc.value.detail == "User already unbanned"


# =========================================================
# ===================== UPDATE TOKENS ======================
# =========================================================

@pytest.mark.asyncio
async def test_update_tokens_success():
    """
    Tokens should reset to 100 and update timestamp
    """
    user = MagicMock(id=1, token=50, last_reset_date=None)
    db = create_mock_db(user)

    await update_tokens(user_id=1, db=db)

    assert user.token == 100
    assert isinstance(user.last_reset_date, datetime)

    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_update_tokens_user_not_found():
    """
    User not found → should raise 404
    """
    db = create_mock_db(None)

    with pytest.raises(HTTPException):
        await update_tokens(user_id=1, db=db)


# =========================================================
# ================= CANCEL SUBSCRIPTION ====================
# =========================================================

@pytest.mark.asyncio
async def test_cancel_subscription_success():
    """
    Premium → Free, tokens reduced safely
    """
    user = MagicMock(id=1, token=500, subscription="premium", last_reset_date=None)
    db = create_mock_db(user)

    await cancel_subscriptions(user_id=1, db=db)

    assert user.subscription == "free"
    assert user.token == 0
    assert isinstance(user.last_reset_date, datetime)


@pytest.mark.asyncio
async def test_cancel_subscription_not_found():
    """
    User not found → 404
    """
    db = create_mock_db(None)

    with pytest.raises(HTTPException):
        await cancel_subscriptions(user_id=1, db=db)


@pytest.mark.asyncio
async def test_cancel_subscription_already_free():
    """
    Already free → 400
    """
    user = MagicMock(id=1, token=500, subscription="free")
    db = create_mock_db(user)

    with pytest.raises(HTTPException):
        await cancel_subscriptions(user_id=1, db=db)


# =========================================================
# ================= RENEW SUBSCRIPTION =====================
# =========================================================

@pytest.mark.asyncio
async def test_renew_subscription_success():
    """
    Free → Premium, tokens increase
    """
    user = MagicMock(id=1, token=100, subscription="free", last_reset_date=None)
    db = create_mock_db(user)

    await renew_subscriptions(user_id=1, db=db)

    assert user.subscription == "premium"
    assert user.token == 600
    assert isinstance(user.last_reset_date, datetime)


@pytest.mark.asyncio
async def test_renew_subscription_not_found():
    """
    User not found → 404
    """
    db = create_mock_db(None)

    with pytest.raises(HTTPException):
        await renew_subscriptions(user_id=1, db=db)


@pytest.mark.asyncio
async def test_renew_subscription_already_premium():
    """
    Already premium → 400
    """
    user = MagicMock(id=1, subscription="premium")
    db = create_mock_db(user)

    with pytest.raises(HTTPException):
        await renew_subscriptions(user_id=1, db=db)