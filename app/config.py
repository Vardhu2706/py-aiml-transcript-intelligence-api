# app/config.py
from typing import Optional

# Try to import the modern pydantic-settings BaseSettings first
try:
    from pydantic_settings import BaseSettings
    PYDANTIC_SETTINGS_AVAILABLE = True
except Exception:
    # Fall back to pydantic v1 / v2 BaseSettings if available
    try:
        from pydantic import BaseSettings  # type: ignore
        PYDANTIC_SETTINGS_AVAILABLE = False
    except Exception:
        raise RuntimeError(
            "Pydantic BaseSettings not available. Install pydantic or pydantic-settings."
        )

from pydantic import Field


if PYDANTIC_SETTINGS_AVAILABLE:
    # Pydantic-settings / Pydantic v2 style using model_config
    class Settings(BaseSettings):
        app_env: str = Field("development", env="APP_ENV")
        api_key: str = Field("changeme", env="API_KEY")

        database_url: str = Field(..., env="DATABASE_URL")
        redis_url: str = Field(..., env="REDIS_URL")

        # Optional conveniences (won't be required)
        postgres_user: Optional[str] = Field(None, env="POSTGRES_USER")
        postgres_password: Optional[str] = Field(None, env="POSTGRES_PASSWORD")
        postgres_db: Optional[str] = Field(None, env="POSTGRES_DB")
        postgres_host: Optional[str] = Field(None, env="POSTGRES_HOST")
        postgres_port: Optional[str] = Field(None, env="POSTGRES_PORT")

        celery_broker_url: Optional[str] = Field(None, env="CELERY_BROKER_URL")
        celery_result_backend: Optional[str] = Field(None, env="CELERY_RESULT_BACKEND")

        # Allow extra env vars from docker-compose
        model_config = {
            "extra": "allow",
            "env_file": ".env",
            "env_file_encoding": "utf-8",
        }

else:
    # Fallback for older pydantic where BaseSettings expects Config inner class
    class Settings(BaseSettings):
        app_env: str = Field("development", env="APP_ENV")
        api_key: str = Field("changeme", env="API_KEY")

        database_url: str = Field(..., env="DATABASE_URL")
        redis_url: str = Field(..., env="REDIS_URL")

        postgres_user: Optional[str] = Field(None, env="POSTGRES_USER")
        postgres_password: Optional[str] = Field(None, env="POSTGRES_PASSWORD")
        postgres_db: Optional[str] = Field(None, env="POSTGRES_DB")
        postgres_host: Optional[str] = Field(None, env="POSTGRES_HOST")
        postgres_port: Optional[str] = Field(None, env="POSTGRES_PORT")

        celery_broker_url: Optional[str] = Field(None, env="CELERY_BROKER_URL")
        celery_result_backend: Optional[str] = Field(None, env="CELERY_RESULT_BACKEND")

        class Config:
            extra = "allow"
            env_file = ".env"
            env_file_encoding = "utf-8"


# instantiate once for import elsewhere
settings = Settings()