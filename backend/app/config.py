"""Application configuration using Pydantic Settings.

Configuration is loaded from environment variables with sensible defaults.
Sensitive values (API keys) have no defaults and must be provided.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Environment
    environment: str = "development"
    debug: bool = False

    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str

    # LLM
    xai_api_key: str | None = None
    use_local_llm: bool = False
    ollama_base_url: str = "http://localhost:11434"

    # Stripe
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_price_seeker: str | None = None
    stripe_price_initiate: str | None = None
    stripe_price_credits: str | None = None

    # CORS - stored as string in env, parsed to list
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Logging
    log_level: str = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from comma-separated string to list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return v
        return v


def get_settings() -> Settings:
    """Get or create settings instance.

    Returns:
        Settings: Application configuration loaded from environment.
    """
    return Settings()  # type: ignore[call-arg]
