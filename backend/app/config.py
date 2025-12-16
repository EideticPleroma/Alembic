"""Application configuration using Pydantic Settings.

Configuration is loaded from environment variables with sensible defaults.
Sensitive values (API keys) have no defaults and must be provided.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(case_sensitive=False)

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

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Logging
    log_level: str = "INFO"


def get_settings() -> Settings:
    """Get or create settings instance.

    Returns:
        Settings: Application configuration loaded from environment.
    """
    return Settings()
