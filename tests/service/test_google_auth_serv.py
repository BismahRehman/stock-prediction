from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from app.config import settings
from app.service.google_auth import login_google, google_callback

# ==============================test_login_google_url=====================================
# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

@pytest.mark.asyncio
async def test_login_google_url_contains_required_params():
    url = await login_google()

    # --- base endpoint ---
    assert "https://accounts.google.com/o/oauth2/v2/auth" in url

    # --- required params ---
    assert f"client_id={settings.CLIENT_ID}" in url
    assert f"redirect_uri={settings.REDIRECT_URI}" in url
    assert "response_type=code" in url
    assert "scope=openid email profile" in url
    assert "access_type=offline" in url
    assert "prompt=consent" in url



 # ==============================test_login_google_url=====================================


from unittest.mock import MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_google_callback_success(monkeypatch):

    mock_user = MagicMock()
    mock_user.email = "test@gmail.com"

    # --- DB FIX ---
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    monkeypatch.setattr(
        "app.repository.google_auth.add_user",
        AsyncMock(return_value=mock_user)
    )

    mock_token_response = MagicMock()
    mock_token_response.json.return_value = {
        "access_token": "google_access_token"
    }

    mock_userinfo_response = MagicMock()
    mock_userinfo_response.json.return_value = {
        "email": "test@gmail.com"
    }

    mock_client = MagicMock()
    mock_client.post = AsyncMock(return_value=mock_token_response)
    mock_client.get = AsyncMock(return_value=mock_userinfo_response)

    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__.return_value = mock_client

        # FIXED HERE
        result = await google_callback("fake_code", mock_db)

    assert result["token_type"] == "bearer"
    assert "access_token" in result



@pytest.mark.asyncio
async def test_google_callback_no_access_token(monkeypatch):

    mock_token_response = MagicMock()
    mock_token_response.json.return_value = {}  # ❌ no token

    mock_client = MagicMock()
    mock_client.post = AsyncMock(return_value=mock_token_response)

    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__.return_value = mock_client

        result = await google_callback("code", MagicMock())

    assert "error" in result
    assert result["error"] == "Failed to obtain access token"