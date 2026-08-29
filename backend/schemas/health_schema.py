from pydantic import BaseModel
from typing import Dict, Any


class HealthPredictionRequest(BaseModel):
    condition: str
    data: Dict[str, Any]