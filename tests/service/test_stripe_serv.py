from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.service.stripe import subscription_checkout, webhook


@pytest.mark.asyncio
async def test_subscription_checkout_existing_customer(monkeypatch):

    mock_user = "test@gmail.com"

    # --- mock existing customer ---
    mock_customer = MagicMock()
    mock_customer.id = "cust_123"

    mock_list = MagicMock()
    mock_list.data = [mock_customer]

    monkeypatch.setattr(
        "stripe.Customer.list_async",
        AsyncMock(return_value=mock_list)
    )

    monkeypatch.setattr(
        "stripe.checkout.Session.create_async",
        AsyncMock(return_value=MagicMock(url="http://checkout.url"))
    )

    result = await subscription_checkout(mock_user)

    assert result == "http://checkout.url"


@pytest.mark.asyncio
async def test_subscription_checkout_stripe_error(monkeypatch):

    monkeypatch.setattr(
        "stripe.Customer.list_async",
        AsyncMock(side_effect=Exception("Stripe error"))
    )

    with pytest.raises(HTTPException) as exc:
        await subscription_checkout("test@gmail.com")

    assert exc.value.status_code == 400







@pytest.mark.asyncio
async def test_webhook_invalid_payload():

    mock_request = MagicMock()
    mock_request.body = AsyncMock(return_value=b"bad_payload")
    mock_request.headers = {"Stripe-Signature": "sig123"}

    with patch("stripe.Webhook.construct_event", side_effect=ValueError):

        with pytest.raises(HTTPException) as exc:
            await webhook(mock_request, MagicMock())

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid payload"


@pytest.mark.asyncio
async def test_webhook_invalid_signature():

    mock_request = MagicMock()
    mock_request.body = AsyncMock(return_value=b"payload")
    mock_request.headers = {"Stripe-Signature": "bad_sig"}

    with patch("stripe.Webhook.construct_event", side_effect=Exception("bad sig")):

        with pytest.raises(HTTPException) as exc:
            await webhook(mock_request, MagicMock())

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid Signature"



@pytest.mark.asyncio
async def test_webhook_checkout_session_completed(monkeypatch):

    # ---- Mock request ----
    mock_request = MagicMock()
    mock_request.body = AsyncMock(return_value=b"payload")
    mock_request.headers = {"Stripe-Signature": "sig123"}

    # ---- Create proper session object (NOT dict) ----
    mock_session = MagicMock()
    mock_session.id = "cs_123"

    # nested attribute: session.customer_details.email
    mock_session.customer_details = MagicMock()
    mock_session.customer_details.email = "test@example.com"

    # ---- Mock Stripe event ----
    mock_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": mock_session   # ✅ object, not dict
        }
    }

    mock_db = MagicMock()

    # ---- Patch Stripe webhook verification ----
    with patch("stripe.Webhook.construct_event", return_value=mock_event):

        # ---- Patch where USED (correct location) ----
        mock_handler = AsyncMock()
        monkeypatch.setattr(
            "app.service.stripe.handle_checkout_session",
            mock_handler
        )

        result = await webhook(mock_request, mock_db)

    # ---- Assertions ----
    assert result is None

    # verify handler was called correctly
    mock_handler.assert_awaited_once_with(mock_session, mock_db)