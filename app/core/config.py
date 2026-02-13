"""
Application configuration module.

Manages environment-driven settings using Pydantic v2.
All sensitive configuration (DB credentials, API keys) must be set via
environment variables or .env file - never hardcoded.

Author: Project
Last Modified: 2026-02-12
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str


settings = Settings()
