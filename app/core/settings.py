from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8"
    )

    app_name: str = "Finance API"
    app_version: str = "1.0.0"
    app_description: str = "Finance API"

    DEBUG: bool = False
    DATABASE_URL: str 
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    
    model_config = SettingsConfigDict(env_file=f"{CORE_DIR}/.env")


settings = Settings()