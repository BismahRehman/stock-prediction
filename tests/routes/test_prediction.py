from fastapi import HTTPException

from app.dependency import get_db, get_current_user, get_token
from app.main import app
from tests.conftest import client
from app.routes import  prediction


def fake_current_user():
    return "test_user"


def fake_get_db():
    return "fake_db"

def fake_get_token():
    return "fake_token"



# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


async def fake_train_stocks(req, token, db, current_user):
    return {
        "AAPL": 0.91,
        "TSLA": 0.87
    }

async def fake_prediction_result(current_user, accuracy_results, model, db):
    return None

def test_train_model(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_token] = fake_get_token



    monkeypatch.setattr(
        "app.routes.prediction.train_stocks",
         fake_train_stocks
    )

    monkeypatch.setattr(
        "app.routes.prediction.prediction_result",
        fake_prediction_result
    )

    payload = {
  "model_name": "random_forest",
  "stocks": [
    "AAPL",
    "TSLA"
  ],
  "features": [
    "OHLC",
    "EMA"
  ],
  "test_size": 0.2,
  "premium_user": False
}

    response = client.post("/prediction/train", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "model_used": "random_forest",
        "accuracy": {
            "AAPL": 0.91,
            "TSLA": 0.87
        }
    }

    app.dependency_overrides = {}



# -----------------------------
# TEST 2: Stock not Selected
# -----------------------------

async def fake_train_stocks_stock_not_selected(req, token, db, current_user):
    raise HTTPException(status_code=400, detail="stock not Selected")


async def fake_prediction_result_stock_not_selected(current_user, accuracy_results, model, db):
    return None


def test_train_model_stock_not_selected(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_token] = fake_get_token

    monkeypatch.setattr(
        "app.routes.prediction.train_stocks",
        fake_train_stocks_stock_not_selected
    )

    monkeypatch.setattr(
        "app.routes.prediction.prediction_result",
        fake_prediction_result_stock_not_selected
    )

    payload = {
        "model_name": "random_forest",
        "stocks": [],
        "features": [
            "OHLC",
            "EMA"
        ],
        "test_size": 0.2,
        "premium_user": False
    }

    response = client.post("/prediction/train", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail" : "stock not Selected"

    }


    app.dependency_overrides = {}





# -----------------------------
# TEST 3: access_premium_model
# -----------------------------

async def fake_train_stocks_access_premium_model(req, token, db, current_user):
    raise HTTPException(status_code=400, detail="stock not Selected")


async def fake_prediction_result_access_premium_model(current_user, accuracy_results, model, db):
    return None


def test_train_model_access_premium_model(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_token] = fake_get_token

    monkeypatch.setattr(
        "app.routes.prediction.train_stocks",
        fake_train_stocks_access_premium_model
    )

    monkeypatch.setattr(
        "app.routes.prediction.prediction_result",
        fake_prediction_result_access_premium_model
    )

    payload = {
        "model_name": "neural_network",
        "stocks": [
            "OHLC",
            "EMA"
        ],
        "features": [
            "OHLC",
            "EMA"
        ],
        "test_size": 0.2,
        "premium_user": False
    }

    response = client.post("/prediction/train", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail" : "stock not Selected"

    }


    app.dependency_overrides = {}



# -----------------------------
# TEST 3: invalid_model_name
# -----------------------------

async def fake_train_stocks_invalid_model_name(req, token, db, current_user):
    raise HTTPException(status_code=400, detail="stock not Selected")


async def fake_prediction_result_invalid_model_name(current_user, accuracy_results, model, db):
    return None


def test_train_model_invalid_model_name(monkeypatch):
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_token] = fake_get_token

    monkeypatch.setattr(
        "app.routes.prediction.train_stocks",
        fake_train_stocks_invalid_model_name
    )

    monkeypatch.setattr(
        "app.routes.prediction.prediction_result",
        fake_prediction_result_invalid_model_name
    )

    payload = {
        "model_name": "neuralnetwork",
        "stocks": [
            "OHLC",
            "EMA"
        ],
        "features": [
            "OHLC",
            "EMA"
        ],
        "test_size": 0.2,
        "premium_user": False
    }

    response = client.post("/prediction/train", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail" : "stock not Selected"

    }


    app.dependency_overrides = {}
