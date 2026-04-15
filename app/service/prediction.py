from typing import Dict
import asyncio
import yfinance as yf

from fastapi import HTTPException
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

from app.dependency import update_token


# -----------------------------------------
# STOCK MODEL TRAINING PIPELINE
# -----------------------------------------
async def train_stocks(req, token, db, current_user) -> Dict[str, float]:

    results: Dict[str, float] = {}

    for stock in req.stocks:
        try:

            # -----------------------------
            # 1. Data ingestion (blocking lib → thread)
            # -----------------------------
            df = await asyncio.to_thread(
                yf.download,
                stock,
                period="1y",
                interval="1d",
                progress=False
            )

            if df.empty:
                results[stock] = None
                continue

            df = df.copy()

            # -----------------------------
            # 2. Feature engineering
            # -----------------------------
            if "EMA" in req.features:
                df["EMA"] = df["Close"].ewm(span=10, adjust=False).mean()

            if "MAR" in req.features:
                df["MAR"] = df["Close"] / df["Close"].ewm(span=10, adjust=False).mean()

            df.dropna(inplace=True)

            # Target variable (next-day prediction)
            df["target"] = df["Close"].shift(-1)
            df.dropna(inplace=True)

            # -----------------------------
            # 3. Feature selection
            # -----------------------------
            cols = []

            if "OHLC" in req.features:
                cols += ["Open", "High", "Low", "Close"]

            if "EMA" in req.features:
                cols.append("EMA")

            if "MAR" in req.features:
                cols.append("MAR")

            if not cols:
                raise HTTPException(
                    status_code=400,
                    detail="No features selected"
                )

            X = df[cols]
            y = df["target"]

            # -----------------------------
            # 4. Train-test split
            # -----------------------------
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=req.test_size,
                shuffle=False
            )

            # -----------------------------
            # 5. Model selection
            # -----------------------------
            try:
                name = req.model_name.lower()

                if name == "random_forest":
                    model = RandomForestRegressor()

                elif name == "linear_regression":
                    model = LinearRegression()

                elif name == "neural_network":
                    if not req.premium_user:
                        raise ValueError("Neural Network is only available for premium users")
                    model = MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=500)

                else:
                    raise ValueError("Invalid model name")

            except ValueError as e:
                message = str(e)

                if "premium" in message.lower():
                    raise HTTPException(status_code=403, detail=message)
                else:
                    raise HTTPException(status_code=400, detail=message)

            # -----------------------------
            # 6. Training (CPU offloaded)
            # -----------------------------
            await asyncio.to_thread(model.fit, X_train, y_train)

            # -----------------------------
            # 7. Prediction
            # -----------------------------
            y_pred = await asyncio.to_thread(model.predict, X_test)

            # -----------------------------
            # 8. Evaluation
            # -----------------------------
            accuracy = await asyncio.to_thread(r2_score, y_test, y_pred)

            results[stock] = round(float(accuracy), 4)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing {stock}: {str(e)}"
            )

    # -----------------------------
    # 9. Token/billing update
    # -----------------------------
    await update_token(current_user, db, token)

    return results