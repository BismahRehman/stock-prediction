
from fastapi import HTTPException

from app.dependency import get_db, get_current_user
from app.main import app
from tests.conftest import client


# @router.post("/webhook")
# async def stripe_webhook(request: Request, db= Depends(get_db)):
#
#     await (webhook(request, db))
#
#     return {"status": "success"}
#
#
# @router.get("/success")
# async def success_page():
#
#     return {"message": "Payment Successful! Thank you for your purchase."}
#
# @router.get("/cancel")
# def cancel_page():
#
#     return {"message": "Payment was cancelled."}

def fake_current_user():
    return "test_user"

def fake_get_db():
    return "fake_db"



# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


async def fake_subscription_checkout(current_user):
    return "https://api.stripe.com/user"

def test_create_subscription_checkout(monkeypatch):

    app.dependency_overrides[get_current_user] = fake_current_user

    monkeypatch.setattr(
        "app.routes.stripe.subscription_checkout",
        fake_subscription_checkout
    )

    response = client.get("/create-subscription-checkout")

    assert response.status_code == 200
    assert response.json() == {
        "session": "https://api.stripe.com/user"
    }



# -------------------------
# TEST 2 :  BAD_Request
# -------------------------


async def fake_subscription_checkout_bad_request(current_user):
    raise HTTPException(status_code=400, detail="Bad Request")


def test_create_subscription_checkout_bad_request(monkeypatch):

    app.dependency_overrides[get_current_user] = fake_current_user

    monkeypatch.setattr(
        "app.routes.stripe.subscription_checkout",
        fake_subscription_checkout_bad_request
    )

    response = client.get("/create-subscription-checkout")

    assert response.status_code == 400
    assert response.json() == {
        "detail" : "Bad Request"
    }

# ============================ webhook==================================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

async def fake_webhook(request, db):
    return None

def test_stripe_webhook(monkeypatch):
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.stripe.webhook",
        fake_webhook
    )
    response = client.post("/webhook")

    assert response.status_code == 200
    assert response.json() == {
        "status": "success"
    }


# -------------------------
# TEST 2: invalid_payload
# -------------------------


async def fake_webhook_invalid_payload(request, db):
    raise  HTTPException(status_code=400, detail="Invalid payload")

def test_stripe_webhook_invalid_payload(monkeypatch):
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.stripe.webhook",
        fake_webhook_invalid_payload
    )
    response = client.post("/webhook")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid payload"
    }



# -------------------------
# TEST 2: invalid_signature
# -------------------------


async def fake_webhook_invalid_signature(request, db):
    raise  HTTPException(status_code=401, detail="invalid_signature")

def test_stripe_webhook_invalid_signature(monkeypatch):
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.stripe.webhook",
        fake_webhook_invalid_signature
    )
    response = client.post("/webhook")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "invalid_signature"
    }

# =========================== Test success API ======================================


def test_success_page():

    response = client.get("/success")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Payment Successful! Thank you for your purchase."
    }




# =========================== Test cancel API ======================================


def test_cancel_page():

    response = client.get("/cancel")
    assert response.status_code == 200

    assert response.json() == {
        "message": "Payment was cancelled."
    }