from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):

    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"
    DEBUG: bool = False

    DATABASE_URL: str
    ENTERPRISE: str
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()