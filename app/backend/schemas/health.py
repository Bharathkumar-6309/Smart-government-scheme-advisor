from pydantic import BaseModel
from typing import Dict, Any


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "ok",
                "version": "1.0.0",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
