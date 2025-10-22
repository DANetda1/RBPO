from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENV: str = "dev"
    ADMIN_TOKEN: Optional[str] = None
    MAX_CONTENT_LENGTH: int = 1 * 1024 * 1024
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()
