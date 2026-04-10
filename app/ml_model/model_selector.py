from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ============================
# Model Selector
# ============================
def get_model(name: str, premium: bool):
    try:
        name = name.lower()

        if name == "random_forest":
            return RandomForestRegressor()

        elif name == "linear_regression":
            return LinearRegression()

        elif name == "neural_network":
            if not premium:
                raise ValueError("Neural Network is only available for premium users")
            return MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=500)

        else:
            raise ValueError("Invalid model name")

    except ValueError as e:
        # Convert internal ValueError to HTTPException with 400 or 403 status code
        message = str(e)
        if "premium" in message.lower():
            raise HTTPException(status_code=403, detail=message)
        else:
            raise HTTPException(status_code=400, detail=message)
