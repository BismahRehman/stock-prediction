#
# from fastapi import HTTPException
#
# from app.service.prediction import train_stocks
# import pytest
# import pandas as pd
# from unittest.mock import MagicMock, AsyncMock
#
# #
#
#
import numpy as np
import pandas as pd
#
#


import pytest
from unittest.mock import MagicMock, AsyncMock

from fastapi import HTTPException

from app.service.prediction import train_stocks


async def fake_update_token(current_user, db, token):
    return None


@pytest.mark.asyncio
async def test_train_stocks_empty_data(monkeypatch):

    import pandas as pd

    # --- empty dataframe ---
    mock_df = pd.DataFrame()

    monkeypatch.setattr(
        "yfinance.download",
        lambda *args, **kwargs: mock_df
    )

    # --- request ---
    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = ["EMA"]
    req.test_size = 0.2
    req.model_name = "random_forest"
    req.premium_user = True

    # --- IMPORTANT: correct patch path ---
    monkeypatch.setattr(
        "app.service.prediction.update_token",
        fake_update_token
    )

    # --- DB MOCK FIX (CRITICAL) ---
    mock_user = MagicMock()
    mock_user.token = 100

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    mock_db = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    # --- CALL ---
    result = await train_stocks(req, 10, mock_db, "user")

    # --- ASSERT ---
    assert result == {"AAPL": None}


@pytest.mark.asyncio
async def test_train_stocks_no_features():

    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = []
    req.test_size = 0.2
    req.model_name = "random_forest"
    req.premium_user = True

    with pytest.raises(HTTPException) as exc:
        await train_stocks(req, "token", MagicMock(), "user")

    assert exc.value.status_code == 400
    assert "No features selected" in str(exc.value.detail)



@pytest.mark.asyncio
async def test_train_stocks_invalid_model():

    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = ["EMA"]
    req.test_size = 0.2
    req.model_name = "invalid_model"
    req.premium_user = True

    with pytest.raises(HTTPException) as exc:
        await train_stocks(req, "token", MagicMock(), "user")

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_train_stocks_premium_required():

    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = ["EMA"]
    req.test_size = 0.2
    req.model_name = "neural_network"
    req.premium_user = False

    # minimal DB (never used but safe)
    mock_db = MagicMock()

    with pytest.raises(Exception) as exc:
        await train_stocks(req, "token", mock_db, "user")

    assert "premium users" in str(exc.value).lower()




@pytest.mark.asyncio
async def test_train_stocks_stock_failure(monkeypatch):

    def fake_download(*args, **kwargs):
        raise Exception("download failed")

    monkeypatch.setattr("yfinance.download", fake_download)

    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = ["EMA"]
    req.test_size = 0.2
    req.model_name = "random_forest"
    req.premium_user = True

    with pytest.raises(HTTPException) as exc:
        await train_stocks(req, "token", MagicMock(), "user")

    assert "Error processing AAPL" in str(exc.value.detail)







@pytest.mark.asyncio
async def test_train_stocks_success(monkeypatch):

    # --------------------
    # 1. FAKE DATA
    # --------------------
    df = pd.DataFrame({
        "Open": [1, 2, 3],
        "High": [1, 2, 3],
        "Low": [1, 2, 3],
        "Close": [1, 2, 3],
    })

    monkeypatch.setattr(
        "yfinance.download",
        lambda *args, **kwargs: df
    )

    # deterministic ML metric
    monkeypatch.setattr(
        "sklearn.metrics.r2_score",
        lambda y, y_pred: 0.91
    )

    # --------------------
    # 2. UPDATE TOKEN MOCK
    # --------------------
    async def fake_update_token(user, db, token):
        return None

    monkeypatch.setattr(
        "app.service.prediction.update_token",
        fake_update_token
    )

    # --------------------
    # 3. MODEL MOCK
    # --------------------
    model_mock = MagicMock()
    model_mock.fit = MagicMock()
    model_mock.predict = MagicMock(return_value=np.array([1, 2]))

    monkeypatch.setattr(
        "sklearn.ensemble.RandomForestRegressor",
        lambda: model_mock
    )

    # --------------------
    # 4. REQUEST
    # --------------------
    req = MagicMock()
    req.stocks = ["AAPL"]
    req.features = ["OHLC"]
    req.test_size = 0.2
    req.model_name = "random_forest"
    req.premium_user = True

    # --------------------
    # 5. DB MOCK (CRITICAL FIX)
    # --------------------
    mock_user = MagicMock()
    mock_user.email = "test@gmail.com"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user

    mock_db = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    # --------------------
    # 6. CALL
    # --------------------
    result = await train_stocks(req, "token", mock_db, mock_user)

    # --------------------
    # 7. ASSERT
    # --------------------
    assert "AAPL" in result
    assert isinstance(result["AAPL"], float)