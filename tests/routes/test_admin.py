from fastapi.testclient import TestClient
from app.main import app
from app.dependency import get_admin, get_db
import app.routes.admin as admin_route

from fastapi import HTTPException
from tests.conftest import client

#
# # create client
# client = TestClient(app)

# -------------------------
# FAKE DEPENDENCIES
# -------------------------

def fake_admin_success():
    return {"id": 1, "role": "admin"}

def fake_admin_fail():
    return {"id": 1, "role": "user"}

def fake_get_db():
    return "fake_db"



def fake_get_admin_forbidden():
    raise HTTPException(status_code=403, detail="Access Denied")

# ========================= Test banned user API ======================================

# -------------------------
# MOCK SERVICE FUNCTION
# -------------------------

async def fake_banned_user(user_id, db):
    return None

# replace real function
admin_route.banned_user = fake_banned_user

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

def test_ban_user_success():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db

    response = client.post("/admin/ban-user/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User banned successfully"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: INVALID INPUT
# -------------------------

def test_ban_user_invalid_id():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db

    response = client.post("/admin/ban-user/abc")

    assert response.status_code == 422

    app.dependency_overrides = {}

# -------------------------
# TEST 3: FORBIDDEN ROLE
# -------------------------

def test_ban_user_forbidden_role():
    app.dependency_overrides[get_admin] = fake_get_admin_forbidden
    app.dependency_overrides[get_db] = fake_get_db

    response = client.post("/admin/ban-user/1")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Access Denied"
    }

    app.dependency_overrides = {}

# ----------------------------
# TEST 4: User Already banned
# ----------------------------

async def fake_banned_user_already_banned(user_id, db):
    raise HTTPException(status_code=400, detail="user already banned")



def test_banned_user_bad_request():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.banned_user = fake_banned_user_already_banned

    response = client.post("/admin/ban-user/1")

    assert response.status_code == 400

    assert response.json() == {
        "detail": "user already banned"
    }

    app.dependency_overrides = {}



# ----------------------------
# TEST 5: User Not Found
# ----------------------------

async def fake_banned_user_not_found(user_id, db):
    raise HTTPException(status_code=404, detail="user not found")

def test_banned_user_not_found():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.banned_user = fake_banned_user_not_found

    response = client.post("/admin/ban-user/1")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "user not found"
    }

    app.dependency_overrides = {}


# # ========================= Test unbanned user API ======================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_unbanned_user(user_id, db):
    return None

def test_unban_user_success():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.unbanned_user = fake_unbanned_user

    response = client.post("/admin/unban-user/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User unbanned successfully"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: INVALID INPUT
# -------------------------

def test_unban_user_invalid_id():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.unbanned_user = fake_unbanned_user


    response = client.post("/admin/unban-user/abc")

    assert response.status_code == 422



    app.dependency_overrides = {}


# -------------------------
# TEST 3: FORBIDDEN ROLE
# -------------------------

def test_unban_user_forbidden_role():
    app.dependency_overrides[get_admin] = fake_get_admin_forbidden
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.unbanned_user = fake_unbanned_user

    response = client.post("/admin/ban-user/1")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Access Denied"
    }

    app.dependency_overrides = {}


# ----------------------------
# TEST 4: User Already banned
# ----------------------------

async def fake_unbanned_user_already_unbanned(user_id, db):
    raise HTTPException(status_code=400, detail="user already unbanned")


def test_unbanned_user_bad_request():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.unbanned_user = fake_unbanned_user_already_unbanned

    response = client.post("/admin/unban-user/1")

    assert response.status_code == 400

    assert response.json() == {
        "detail": "user already unbanned"
    }

    app.dependency_overrides = {}




# ----------------------------
# TEST 5: User Not Found
# ----------------------------

async def fake_unbanned_user_not_found(user_id, db):
    raise HTTPException(status_code=404, detail="user not found")


def test_unbanned_user_not_found():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.unbanned_user= fake_unbanned_user_not_found

    response = client.post("/admin/unban-user/1")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "user not found"
    }

    app.dependency_overrides = {}


# ========================= Test update token  API ======================================


# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_update_token(user_id, db):
    return None

def test_update_token_success():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.update_tokens= fake_update_token

    response = client.post("/admin/update-tokens/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User Token Update successfully"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: INVALID INPUT
# -------------------------

def test_update_token_invalid_id():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.update_tokens = fake_update_token


    response = client.post("/admin/update-tokens/abc")

    assert response.status_code == 422

    app.dependency_overrides = {}


# -------------------------
# TEST 3: FORBIDDEN ROLE
# -------------------------

def test_update_token_forbidden_role():
    app.dependency_overrides[get_admin] = fake_get_admin_forbidden
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.update_token = fake_update_token


    response = client.post("/admin/update-tokens/1")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Access Denied"
    }

    app.dependency_overrides = {}


# ----------------------------
# TEST 4: User Not Found
# ----------------------------

async def fake_update_token_user_not_found(user_id, db):
    raise HTTPException(status_code=404, detail="user not found")


def test_update_token_user_not_found():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.update_tokens = fake_update_token_user_not_found

    response = client.post("/admin/update-tokens/1")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "user not found"
    }

    app.dependency_overrides = {}



# # ========================= Test cancel_subscription API ======================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_cancel_subscription(user_id, db):
    return None

def test_cancel_subscription_success():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.cancel_subscriptions = fake_cancel_subscription

    response = client.post("/admin/cancel-subscription/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User subscription Update successfully"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: INVALID INPUT
# -------------------------

def test_cancel_subscription_invalid_id():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.cancel_subscriptions = fake_cancel_subscription


    response = client.post("/admin/cancel-subscription/abc")

    assert response.status_code == 422

    app.dependency_overrides = {}


# -------------------------
# TEST 3: FORBIDDEN ROLE
# -------------------------

def test_cancel_subscription_forbidden_role():
    app.dependency_overrides[get_admin] = fake_get_admin_forbidden
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.cancel_subscriptions = fake_cancel_subscription

    response = client.post("/admin/cancel-subscription/1")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Access Denied"
    }

    app.dependency_overrides = {}


# ----------------------------
# TEST 4: User Already banned
# ----------------------------

async def fake_cancel_subscription_already_cancel(user_id, db):
    raise HTTPException(status_code=400, detail="User already in free tier subscription")


def test_cancel_subscription_bad_request():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.cancel_subscriptions = fake_cancel_subscription_already_cancel

    response = client.post("/admin/cancel-subscription/1")

    assert response.status_code == 400

    assert response.json() == {
        "detail": "User already in free tier subscription"
    }

    app.dependency_overrides = {}




# ----------------------------
# TEST 5: User Not Found
# ----------------------------

async def fake_cancel_subscription_user_not_found(user_id, db):
    raise HTTPException(status_code=404, detail="user not found")


def test_cancel_subscription_user_not_found():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.cancel_subscriptions= fake_cancel_subscription_user_not_found

    response = client.post("/admin/cancel-subscription/1")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "user not found"
    }

    app.dependency_overrides = {}


# # ========================= Test renew_subscription API ======================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_renew_subscription(user_id, db):
    return None

def test_renew_subscription_success():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.renew_subscriptions = fake_renew_subscription

    response = client.post("/admin/renew-subscription/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User subscription Update successfully"
    }

    app.dependency_overrides = {}


# -------------------------
# TEST 2: INVALID INPUT
# -------------------------

def test_renew_subscription_invalid_id():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.renew_subscriptions = fake_renew_subscription


    response = client.post("/admin/renew-subscription/abc")

    assert response.status_code == 422

    app.dependency_overrides = {}


# -------------------------
# TEST 3: FORBIDDEN ROLE
# -------------------------

def test_renew_subscription_forbidden_role():
    app.dependency_overrides[get_admin] = fake_get_admin_forbidden
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.renew_subscriptions = fake_renew_subscription

    response = client.post("/admin/renew-subscription/1")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Access Denied"
    }

    app.dependency_overrides = {}


# ----------------------------
# TEST 4: User Already banned
# ----------------------------

async def fake_renew_subscription_already_renew(user_id, db):
    raise HTTPException(status_code=400, detail="User already in premium tier subscription")


def test_renew_subscription_bad_request():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.renew_subscriptions =fake_renew_subscription_already_renew

    response = client.post("/admin/renew-subscription/1")

    assert response.status_code == 400

    assert response.json() == {
        "detail": "User already in premium tier subscription"
    }

    app.dependency_overrides = {}




# ----------------------------
# TEST 5: User Not Found
# ----------------------------

async def fake_renew_subscription_user_not_found(user_id, db):
    raise HTTPException(status_code=404, detail="user not found")


def test_renew_subscription_user_not_found():
    app.dependency_overrides[get_admin] = fake_admin_success
    app.dependency_overrides[get_db] = fake_get_db
    admin_route.renew_subscriptions= fake_renew_subscription_user_not_found

    response = client.post("/admin/renew-subscription/1")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "user not found"
    }

    app.dependency_overrides = {}

