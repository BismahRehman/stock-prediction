# train_service.py

from typing import Dict
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from fastapi import HTTPException

from app.dependency import update_token
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

import asyncio


async def train_stocks(req, token, db, current_user) -> Dict[str, float]:
    results: Dict[str, float] = {}

    for stock in req.stocks:
        try:
            # Fetch Data
            df = await asyncio.to_thread( yf.download,stock, period="1y", interval="1d", progress=False)

            if df.empty:
                results[stock] = None
                continue

            # Add features
            #  add_features(df, req.features)

            df = df.copy()

            if "EMA" in req.features:
                df["EMA"] = df["Close"].ewm(span=10, adjust=False).mean()

            if "MAR" in req.features:
                df["MAR"] = df["Close"] / df["Close"].ewm(span=10, adjust=False).mean()

            df.dropna(inplace=True)


            # Target
            df["target"] = df["Close"].shift(-1)
            df.dropna(inplace=True)

            # Select columns
            cols = []
            if "OHLC" in req.features:
                cols += ["Open", "High", "Low", "Close"]
            if "EMA" in req.features:
                cols.append("EMA")
            if "MAR" in req.features:
                cols.append("MAR")

            if not cols:
                raise HTTPException(status_code=400, detail="No features selected")

            X = df[cols]
            y = df["target"]

            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=req.test_size, shuffle=False
            )


            try:
                name = req.model_name.lower()

                if name == "random_forest":
                    model= RandomForestRegressor()

                elif name == "linear_regression":
                    model = LinearRegression()

                elif name == "neural_network":
                    if not req.premium_user:
                        raise ValueError("Neural Network is only available for premium users")
                    model=  MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=500)

                else:
                    raise ValueError("Invalid model name")

            except ValueError as e:
                # Convert internal ValueError to HTTPException with 400 or 403 status code
                message = str(e)
                if "premium" in message.lower():
                    raise HTTPException(status_code=403, detail=message)
                else:
                    raise HTTPException(status_code=400, detail=message)

            # Train in thread
            await asyncio.to_thread(model.fit, X_train, y_train)

            # Predict
            # y_pred = model.predict(X_test)
            y_pred = await asyncio.to_thread(model.predict, X_test)

            # Accuracy
            # accuracy = r2_score(y_test, y_pred)
            accuracy = await asyncio.to_thread(r2_score, y_test, y_pred)
            results[stock] = round(float(accuracy), 4)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing {stock}: {str(e)}")

    await update_token(current_user, db, token)

    return results