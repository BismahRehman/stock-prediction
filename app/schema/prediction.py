
from pydantic import BaseModel, Field
from typing import List, Dict

from starlette.responses import Response


# ============================
# Request Schema
# ============================
class RequestModel(BaseModel):
    model_name: str = Field (..., example="random_forest")  # random_forest, linear_regression, neural_network
    stocks: List[str] = Field (..., example=["AAPL", "TSLA"])
    features: List[str] = Field ( ..., example=["OHLC", "EMA"])
    test_size: float = Field(..., gt=0.0, lt=1.0)
    premium_user: bool = False


class TrainResponse(BaseModel):
    model_used: str
    accuracy: Dict[str, float]