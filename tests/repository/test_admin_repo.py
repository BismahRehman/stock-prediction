#
# async def banned_user( user_id,db):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
#     if user.banned:
#         raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already banned")
#     if  not user.banned:
#         user.banned = True
#     await db.commit()
#     await db.refresh(user)
from datetime import datetime

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from app.repository.admin import banned_user, unbanned_user, update_tokens, cancel_subscriptions, renew_subscriptions


# ===================================== banned user ====================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

@pytest.mark.asyncio
async def test_banned_user_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    await banned_user(user_id=1, db=mock_db)

    # --- Assertions ---
    assert mock_user.banned is True
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)


# -------------------------
# TEST 2: user_not_found
# -------------------------

@pytest.mark.asyncio
async def test_banned_user_not_found():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       await banned_user(user_id=1, db=mock_db)

    # --- Assertions ---

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

# -------------------------
# TEST 3: BANNED USER
# -------------------------

@pytest.mark.asyncio
async def test_banned_user_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = True

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       await banned_user(user_id=1, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 400
    assert exc.value.detail == "User already banned"


# ===================================== unbanned user ====================================


# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

@pytest.mark.asyncio
async def test_unbanned_user_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = True

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    await unbanned_user(user_id=1, db=mock_db)

    # --- Assertions ---
    assert mock_user.banned is False
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)


# -------------------------
# TEST 2: user_not_found
# -------------------------

@pytest.mark.asyncio
async def test_unbanned_user_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = True

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
      await unbanned_user(user_id=1, db=mock_db)

    # --- Assertions ---

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


# -------------------------
# TEST 3: BANNED USER
# -------------------------

@pytest.mark.asyncio
async def test_unbanned_user_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
      await unbanned_user(user_id=1, db=mock_db)

    # --- Assertions ---

    assert exc.value.status_code == 400
    assert exc.value.detail == "User already unbanned"



# ===================================== TEST UPDATE USER TOKEN ====================================
#
# async def update_tokens( user_id,db):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
#     user.token = 100
#     user.last_reset_date = datetime.utcnow()
#
#     await db.commit()
#     await db.refresh(user)
#


# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------
@pytest.mark.asyncio
async def test_update_tokens_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 50
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
    await update_tokens(user_id=1, db=mock_db)

    # --- Assertions ---
    assert mock_user.token == 100
    assert isinstance(mock_user.last_reset_date, datetime)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)
# -------------------------
# TEST 2: user_not_found
# -------------------------

@pytest.mark.asyncio
async def test_update_tokens_user_not_founds():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 100
    mock_user.last_reset_date = None

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
     await update_tokens(user_id=1, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
# -------------------------
# ===================================== TEST CANCEL SUBSCRIPTION ====================================

# async def cancel_subscriptions( user_id,db):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
#     if user.subscription == "free":
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already in free tier subscription ")
#
#     user.subscription = "free"
#     user.token = user.token - 500
#     if user.token <0:
#         user.token = 0
#     user.last_reset_date = datetime.utcnow()
#
#     await db.commit()
#     await db.refresh(user)

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


@pytest.mark.asyncio
async def test_cancel_subscriptions_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 500
    mock_user.subscription = "premium"
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
    await cancel_subscriptions(user_id=1, db=mock_db)

    # --- Assertions ---
    assert mock_user.token == 0
    assert mock_user.subscription == "free"
    assert isinstance(mock_user.last_reset_date, datetime)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)




# -------------------------
# TEST 2: user_not_found
# -------------------------

@pytest.mark.asyncio
async def test_cancel_subscriptions_user_not_found():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 500
    mock_user.subscription = "premium"
    mock_user.last_reset_date = None

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
      await cancel_subscriptions(user_id=1, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


# -----------------------------
# TEST 3: already_cancel
# -----------------------------

@pytest.mark.asyncio
async def test_cancel_subscriptions_already_cancel():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 500
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
    with pytest.raises(HTTPException) as exc:
      await cancel_subscriptions(user_id=1, db=mock_db)


    # --- Assertions ---
    assert exc.value.status_code == 400
    assert exc.value.detail == "User already in free tier subscription "

# ===================================== TEST USER RENEW SUBSCRIPTION ====================================
# async def renew_subscriptions(user_id, db):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     if user.subscription == "premium":
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in premium tier subscription ")
#
#     user.subscription = "premium"
#     user.token = user.token + 500
#     user.last_reset_date =datetime.utcnow()
#
#     await db.commit()
#     await db.refresh(user)

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


@pytest.mark.asyncio
async def test_renew_subscriptions_success():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
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
    await renew_subscriptions(user_id=1, db=mock_db)

    # --- Assertions ---
    assert mock_user.token == 600
    assert mock_user.subscription == "premium"
    assert isinstance(mock_user.last_reset_date, datetime)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(mock_user)




# -------------------------
# TEST 2: user_not_found
# -------------------------

@pytest.mark.asyncio
async def test_renew_subscriptions_user_not_found():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 500
    mock_user.subscription = "free"
    mock_user.last_reset_date = None

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
      await renew_subscriptions(user_id=1, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


# -----------------------------
# TEST 3: already_cancel
# -----------------------------

@pytest.mark.asyncio
async def test_renew_subscriptions_already_cancel():
    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.token = 500
    mock_user.subscription = "premium"
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
    with pytest.raises(HTTPException) as exc:
      await renew_subscriptions(user_id=1, db=mock_db)


    # --- Assertions ---
    assert exc.value.status_code == 400
    assert exc.value.detail == "User already in premium tier subscription "
#