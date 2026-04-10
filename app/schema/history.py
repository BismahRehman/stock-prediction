from typing import Dict

from pydantic import BaseModel


class ResponseHistory(BaseModel):
    model_name:str
    accuracy: Dict[str, float]