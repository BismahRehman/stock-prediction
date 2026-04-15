
from app.dependency import get_db
from app.main import app
from tests.conftest import client
import app.routes.google_auth as google_auth_route

def fake_get_db():
    return "fake_db"


# # ========================= Test login_with_google API ======================================


async def fake_login_google():

    return "https://accounts.google.com/o/oauth2/v2/auth?client_id=731301366951-glk5e0p4vjfa3fhfo4okaendsff94l07.apps.googleusercontent.com&redirect_uri=http://localhost:8000/auth/google/callback&response_type=code&scope=openid email profile&access_type=offline&prompt=consent"

def test_login_with_google():

    response = client.get("/auth/google/login")
    google_auth_route.login_google = fake_login_google


    assert response.status_code == 200
    assert response.json() == {
        "url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=731301366951-glk5e0p4vjfa3fhfo4okaendsff94l07.apps.googleusercontent.com&redirect_uri=http://localhost:8000/auth/google/callback&response_type=code&scope=openid email profile&access_type=offline&prompt=consent"
    }

    # cleanup (important for isolation)
    google_auth_route.login_google = None



# # ========================= Test callback API ======================================


async def fake_google_callback(code, db):
        return {
        "access_token": "fake_access",
        "token_type": "bearer"
    }

def test_google_callback_success():

    app.dependency_overrides[get_db] = fake_get_db

    google_auth_route.google_callback= fake_google_callback

    # Act
    response = client.get("/auth/google/callback?code=asdf")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "fake_access",
        "token_type": "bearer"
    }

    # Cleanup
    app.dependency_overrides = {}