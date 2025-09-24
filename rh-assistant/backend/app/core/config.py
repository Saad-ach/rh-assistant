from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Make keys optional with safe defaults to avoid import-time crashes in dev
    OPENAI_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
