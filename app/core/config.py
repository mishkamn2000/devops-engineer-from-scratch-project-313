from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "URL Shortener"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DATABASE_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    BASE_URL: str = "http://localhost:8080"
    
    class Config:
        env_file = ".env"

settings = Settings()
