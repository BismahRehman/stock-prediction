from fastapi import HTTPException

from app.dependency import get_db
from app.main import app
from tests.conftest import client



async def fake_get_db():
    return "fake_db"



# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_loginuser(user, db):
    return {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzc2MDg4ODczfQ.yb6oBLdmi8CASwJUh4YA0TqHiPYZh2LkLdGdFlgmv6o",
  "token_type": "bearer"}

def test_login(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.loginuser",
        fake_loginuser
    )

    payload = {
        "email": "user@example.com",
        "password": "string"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzc2MDg4ODczfQ.yb6oBLdmi8CASwJUh4YA0TqHiPYZh2LkLdGdFlgmv6o",
        "token_type": "bearer"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: USER NOT FOUND
# -------------------------


async def fake_login_user_not_found(user, db):
   raise HTTPException(status_code=404, detail="User not found")

def test_login_user_not_found(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.loginuser",
        fake_login_user_not_found
    )

    payload = {
        "email": "user@example.com",
        "password": "string"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 404
    assert response.json() == {
       "detail": "User not found"
    }

    app.dependency_overrides = {}



# -------------------------
# TEST 3: USER BANNED
# -------------------------


async def fake_login_user_banned(user, db):
   raise HTTPException(status_code=401, detail="User banned")

def test_login_user_banned(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.loginuser",
        fake_login_user_banned
    )

    payload = {
        "email": "user@example.com",
        "password": "string"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json() == {
       "detail": "User banned"
    }

    app.dependency_overrides = {}


# ---------------------------
# TEST 4: INCORRECT PASSWORD
# ----------------------------


async def fake_login_incorrect_password(user, db):
   raise HTTPException(status_code=401, detail="User entered incorrect password")

def test_login_incorrect_password(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.loginuser",
        fake_login_incorrect_password
    )

    payload = {
        "email": "user@example.com",
        "password": "string"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json() == {
       "detail": "User entered incorrect password"
    }

    app.dependency_overrides = {}

# ---------------------------
# TEST 5: INVALID EMAIL
# ----------------------------


def test_login_invalid_email(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.loginuser",
        fake_loginuser
    )

    payload = {
        "email": "userexample.com",
        "password": "string"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 422

    app.dependency_overrides = {}

# ================================REGISTER USER =============================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_createuser(user, db):
    return None

def test_register(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.createuser",
        fake_createuser
    )

    payload = {

            "email": "user1@example.com",
            "password": "string"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "message": "User registered successfully"
    }

    app.dependency_overrides = {}

# -------------------------
# TEST 2 : INVALID EMAIL
# -------------------------

async def fake_createuser_invalid_email(user, db):
    return None

def test_register_invalid_email(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.createuser",
        fake_createuser_invalid_email
    )

    payload = {

            "email": "user1example.com",
            "password": "string"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422

    app.dependency_overrides = {}

# ----------------------------
# TEST 3 : User Already Exist
# ----------------------------

async def fake_createuser_user_already_exist(user, db):
    raise HTTPException(status_code=409, detail="User already exists")

def test_register_user_already_exist(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.createuser",
        fake_createuser_user_already_exist
    )

    payload = {

            "email": "user1@example.com",
            "password": "string"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json() == {
        "detail": "User already exists"
    }

    app.dependency_overrides = {}


# ----------------------------
# TEST 4 : User Banned
# ----------------------------

async def fake_createuser_user_banned(user, db):
    raise HTTPException(status_code=401, detail="User banned")

def test_register_user_banned(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.user.createuser",
        fake_createuser_user_banned
    )

    payload = {

            "email": "user1@example.com",
            "password": "string"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 401
    assert response.json() == {
        "detail": "User banned"
    }

    app.dependency_overrides = {}





# =================================== TEST logout API ======================================

# # ----------------------------
# TEST 1 : Success
# ----------------------------

async def fake_logout_user(credentials, db):
    return None
def fake_security():
    return

def test_logout(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[fake_security] = fake_security

    monkeypatch.setattr(
        "app.routes.user.logout_user",
        fake_logout_user
    )

    response = client.get("/auth/logout", headers={"Authorization": "Bearer testtoken"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Logged out successfully"
    }

    app.dependency_overrides = {}

