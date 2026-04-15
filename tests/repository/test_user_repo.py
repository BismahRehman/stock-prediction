# async def loginuser(user,db):
#     result = await db.execute(select(User).where(User.email == user.email))
#     db_user = result.scalar_one_or_none()
#
#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_404, detail="User Not Found")
#     if db_user.banned:
#         raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="User is banned")
#
#     if not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect password for user",
#         )
#     token = create_access_token({"sub": user.email})
#
#     return {"access_token": token, "token_type": "bearer"}
#
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi import HTTPException

from app.repository.user import loginuser, createuser, logout_user


# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

def fake_verify_password(user_password, db_user_hashed_password):
    return True
def fake_create_access_token(data: dict):
    return "fake_token"

@pytest.mark.asyncio
async def test_loginuser_success(monkeypatch):
    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock DB user ---
    mock_db_user = MagicMock()
    mock_db_user.email = "test@gmail.com"
    mock_db_user.hashed_password = "hashed"
    mock_db_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_db_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Mock external functions ---
    monkeypatch.setattr(
        "app.repository.user.verify_password",
        fake_verify_password
    )

    monkeypatch.setattr(
        "app.repository.user.create_access_token",
         fake_create_access_token
    )

    # --- Call function ---
    result = await loginuser(mock_input_user, mock_db)

    # --- Assertions ---
    assert result["access_token"] == "fake_token"
    assert result["token_type"] == "bearer"



# ----------------------------
# TEST 2: password not verify
# ----------------------------

def fake_not_verify_password(user_password, db_user_hashed_password):
    return False
def fake_create_access_tokens(data: dict):
    return "fake_token"

@pytest.mark.asyncio
async def test_loginuser_not_verify_password(monkeypatch):
    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock DB user ---
    mock_db_user = MagicMock()
    mock_db_user.email = "test@gmail.com"
    mock_db_user.hashed_password = "hashed"
    mock_db_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_db_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Mock external functions ---
    monkeypatch.setattr(
        "app.repository.user.verify_password",
        fake_not_verify_password
    )

    monkeypatch.setattr(
        "app.repository.user.create_access_token",
         fake_create_access_tokens
    )

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       result =  await loginuser(mock_input_user, mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect password for user"


# ----------------------------
# TEST 3: banned user
# ----------------------------

@pytest.mark.asyncio
async def test_loginuser_banned_user(monkeypatch):
    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock DB user ---
    mock_db_user = MagicMock()
    mock_db_user.email = "test@gmail.com"
    mock_db_user.hashed_password = "hashed"
    mock_db_user.banned = True

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_db_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Mock external functions ---
    monkeypatch.setattr(
        "app.repository.user.verify_password",
        fake_not_verify_password
    )

    monkeypatch.setattr(
        "app.repository.user.create_access_token",
         fake_create_access_tokens
    )

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       result =  await loginuser(mock_input_user, mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 401
    assert exc.value.detail == "User is banned"

# ----------------------------
# TEST 4: user not found
# ----------------------------

@pytest.mark.asyncio
async def test_loginuser_not_verify_password(monkeypatch):
    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock DB user ---
    mock_db_user = MagicMock()
    mock_db_user.email = "test@gmail.com"
    mock_db_user.hashed_password = "hashed"
    mock_db_user.banned = False

    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # --- Mock external functions ---
    monkeypatch.setattr(
        "app.repository.user.verify_password",
        fake_verify_password
    )

    monkeypatch.setattr(
        "app.repository.user.create_access_token",
         fake_create_access_tokens
    )

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       result =  await loginuser(mock_input_user, mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 404
    assert exc.value.detail == "User Not Found"



#
# async def createuser(user,db):
#     result = await db.execute(select(User).where(User.email == user.email))
#     db_user = result.scalar_one_or_none()
#     if db_user:
#         if db_user.banned:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="your account is temporary restricted")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
#
#     hashed_password = hash_password(user.password)
#
#     new_user = User(email=user.email, hashed_password=hashed_password)
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------
def fake_hash_password(user_password):
    return "hash_password"

@pytest.mark.asyncio
async def test_createuser_success(monkeypatch):

    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"
    # --- Mock user ---
    mock_user = MagicMock()


    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    monkeypatch.setattr(
        "app.repository.user.hash_password",
        fake_hash_password
    )

    # --- Call function ---
    await createuser(user=mock_input_user, db=mock_db)

    # --- Assertions ---
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


# -------------------------
# TEST 2: user banned
# -------------------------


@pytest.mark.asyncio
async def test_createuser_banned(monkeypatch):

    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.banned = True


    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    monkeypatch.setattr(
        "app.repository.user.hash_password",
        fake_hash_password
    )

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       await createuser(user=mock_input_user, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 401
    assert exc.value.detail == "your account is temporary restricted"


# -------------------------
# TEST 3: user exist
# -------------------------


@pytest.mark.asyncio
async def test_createuser_exist(monkeypatch):

    # --- Mock input user ---
    mock_input_user = MagicMock()
    mock_input_user.email = "test@gmail.com"
    mock_input_user.password = "plainpassword"

    # --- Mock user ---
    mock_user = MagicMock()
    mock_user.banned = False


    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    monkeypatch.setattr(
        "app.repository.user.hash_password",
        fake_hash_password
    )

    # --- Call function ---
    with pytest.raises(HTTPException) as exc:
       await createuser(user=mock_input_user, db=mock_db)

    # --- Assertions ---
    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already registered"



#
#
# async def logout_user(credentials, db):
#     token = credentials.credentials
#
#     db_token = BlacklistedToken(token=token)
#     db.add(db_token)
#     await db.commit()
#
#     return {"message": "Logged out successfully"}

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

@pytest.mark.asyncio
async def test_logout_user_success(monkeypatch):

    # --- Mock input user ---
    mock_credentials = MagicMock()
    mock_credentials.credentials = "credentials"


    # --- Mock DB result ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    # --- Mock DB ---
    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()



    # --- Call function ---
    await logout_user(credentials= mock_credentials, db=mock_db)

    # --- Assertions ---
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()

