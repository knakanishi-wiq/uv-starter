"""Configuration management using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(default="uv-starter", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    # Database settings (example)
    database_url: str = Field(
        default="sqlite:///./app.db", description="Database connection URL"
    )

    # API settings (example)
    api_host: str = Field(default="localhost", description="API host")
    api_port: int = Field(default=8000, description="API port")

    # External services (example)
    api_key: str = Field(default="", description="External API key")
    secret_key: str = Field(
        default="dev-secret-key", description="Application secret key"
    )

    @field_validator("api_port")
    @classmethod
    def validate_port(cls, v):
        """Validate that port is in valid range 1-65535."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience export
settings = get_settings()
