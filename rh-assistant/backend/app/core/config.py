from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Make keys optional with safe defaults to avoid import-time crashes in dev
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "eubia-local-development-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEMO_AUTH_ENABLED: bool = False
    REDIS_URL: str = "redis://localhost:6379/0"
    APP_NAME: str = "EUBIA HR Assistant"
    APP_DEFAULT_LANGUAGE: str = "de"
    DOCUMENT_STORAGE_MODE: str = "local"
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_ACCOUNT_URL: Optional[str] = None
    AZURE_STORAGE_CONTAINER: str = "hr-documents"
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-10-21"
    AZURE_OPENAI_CHAT_DEPLOYMENT: Optional[str] = None
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: Optional[str] = None
    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_TIMEOUT_SECONDS: float = 45.0
    DOCUMENT_RELEVANCE_DISTANCE: float = 21.8


settings = Settings()

if settings.SECRET_KEY == "eubia-local-development-secret-change-me" and not settings.DEMO_AUTH_ENABLED:
    raise RuntimeError("SECRET_KEY must be configured when DEMO_AUTH_ENABLED is false")
