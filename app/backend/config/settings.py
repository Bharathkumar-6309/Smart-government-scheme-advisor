from pydantic import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    app_name: str = "Smart Government Scheme Advisor"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS settings
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
