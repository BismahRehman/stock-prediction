
from app.dependency import get_current_user, get_db
from app.main import app
from tests.conftest import client


def fake_current_user():
    return "test_user"

def fake_get_db():
    return "fake_db"


# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


async def fake_user_history_success(db, current_user):
    return [
  {
    "model_name": "random_forest",
    "accuracy": {
      "AAPL": 0.7143,
      "TSLA": 0.4928
    }
  },
  {
    "model_name": "random_forest",
    "accuracy": {
      "AAPL": 0.7264,
      "TSLA": 0.4314
    }
  }
]

def test_history_success(monkeypatch):

    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_db] = fake_get_db

    monkeypatch.setattr(
        "app.routes.history.user_history",
        fake_user_history_success
    )

    response = client.get("/prediction/history")

    assert response.status_code == 200
    assert response.json() == [
  {
    "model_name": "random_forest",
    "accuracy": {
      "AAPL": 0.7143,
      "TSLA": 0.4928
    }
  },
  {
    "model_name": "random_forest",
    "accuracy": {
      "AAPL": 0.7264,
      "TSLA": 0.4314
    }
  }
]

    app.dependency_overrides = {}



# -------------------------
# TEST 2: SUCCESS CASE
# -------------------------

