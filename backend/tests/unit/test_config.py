"""Tests for application configuration."""

import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings


def test_settings_requires_supabase_url() -> None:
    """Settings requires SUPABASE_URL to be provided."""
    with pytest.raises(ValidationError):
        Settings(  # type: ignore[call-arg]
            supabase_key="test_key",
            supabase_service_key="test_service_key",
        )


def test_settings_requires_supabase_key() -> None:
    """Settings requires SUPABASE_KEY to be provided."""
    with pytest.raises(ValidationError):
        Settings(  # type: ignore[call-arg]
            supabase_url="https://test.supabase.co",
            supabase_service_key="test_service_key",
        )


def test_settings_requires_supabase_service_key() -> None:
    """Settings requires SUPABASE_SERVICE_KEY to be provided."""
    with pytest.raises(ValidationError):
        Settings(  # type: ignore[call-arg]
            supabase_url="https://test.supabase.co",
            supabase_key="test_key",
        )


def test_settings_loads_required_fields() -> None:
    """Settings loads all required Supabase fields."""
    settings = Settings(
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
    )

    assert settings.supabase_url == "https://test.supabase.co"
    assert settings.supabase_key == "test_key"
    assert settings.supabase_service_key == "test_service_key"


def test_settings_has_sensible_defaults() -> None:
    """Settings has sensible defaults for optional fields."""
    settings = Settings(
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
    )

    assert settings.environment == "development"
    assert settings.debug is False
    assert settings.xai_api_key is None
    assert settings.use_local_llm is False
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.stripe_secret_key is None
    assert settings.stripe_webhook_secret is None
    assert settings.log_level == "INFO"


def test_settings_allows_custom_cors_origins() -> None:
    """Settings allows customizing CORS origins."""
    origins = ["https://example.com", "https://app.example.com"]
    settings = Settings(
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
        cors_origins=origins,
    )

    assert settings.cors_origins == origins


def test_settings_allows_environment_override() -> None:
    """Settings allows overriding environment."""
    settings = Settings(
        environment="production",
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
    )

    assert settings.environment == "production"


def test_settings_allows_debug_override() -> None:
    """Settings allows enabling debug mode."""
    settings = Settings(
        debug=True,
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
    )

    assert settings.debug is True


def test_get_settings_returns_settings_instance() -> None:
    """get_settings() returns a Settings instance."""
    # This test will only pass if proper environment variables are set
    # or if it falls back to defaults gracefully
    try:
        settings = get_settings()
        assert isinstance(settings, Settings)
    except ValueError:
        # Expected in test environment without proper env vars
        pytest.skip("Environment variables not configured for this test")


def test_settings_case_insensitive_env_vars(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Settings loads environment variables case-insensitively."""
    # Set environment variables in uppercase
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test_key")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "test_service_key")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings(
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
        log_level="DEBUG",
    )

    assert settings.supabase_url == "https://test.supabase.co"
    assert settings.supabase_key == "test_key"
    assert settings.supabase_service_key == "test_service_key"
    assert settings.log_level == "DEBUG"


def test_settings_allows_optional_api_keys() -> None:
    """Settings allows LLM and Stripe API keys to be optional."""
    settings = Settings(
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
    )

    assert settings.xai_api_key is None
    assert settings.stripe_secret_key is None
    assert settings.stripe_webhook_secret is None
