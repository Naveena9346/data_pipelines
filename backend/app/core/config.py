import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DataForge Enterprise Data Pipelines Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security & JWT
    SECRET_KEY: str = "dataforge_super_secret_development_key_change_in_production_32bytes"
    ENCRYPTION_KEY: str = "dataforge_aes_secret_key_32_bytes_long!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./dataforge.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./dataforge.db"
    SYNC_DATABASE_URL: str = "sqlite:///./dataforge.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis & Task Queue
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # Storage Settings
    DATA_STORAGE_PATH: str = "./data_storage"
    UPLOAD_TEMP_DIR: str = "./uploads"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

os.makedirs(settings.DATA_STORAGE_PATH, exist_ok=True)
os.makedirs(settings.UPLOAD_TEMP_DIR, exist_ok=True)
