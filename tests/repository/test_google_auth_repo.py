# sync def add_user(db, email,userinfo):
#
#     result = await db.execute(select(User).where(User.email == email))
#     user = result.scalar_one_or_none()
#
#     if not user:
#         user = User(
#             email=email,
#             google_id=userinfo.get("sub"),  # Google’s unique user ID
#             auth_provider="google"
#
#             # other fields as needed
#         )
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)
#
#     return user
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi import HTTPException

from app.repository.google_auth import add_user

# -------------------------
# TEST 2: IF USER NOT EXIST
# -------------------------
@pytest.mark.asyncio
async def test_add_user():
    # --- Mock user ---
    mock_user = MagicMock()

    userinfo = {"sub": "google123"}
    email = "test@example.com"

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---

    await add_user(db=mock_db, email=email, userinfo=userinfo)

    # --- Assertions ---
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()



# -------------------------
# TEST 1: IF USER NOT EXIST
# -------------------------
@pytest.mark.asyncio
async def test_add_user_exist():
    # --- Mock user ---
    existing_user = MagicMock()
    existing_user.email = "test@example.com"

    userinfo = {"sub": "google123"}
    email = "test@example.com"

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Call function ---

    await add_user(db=mock_db, email=email, userinfo=userinfo)

    # --- should NOT create new user ---
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()