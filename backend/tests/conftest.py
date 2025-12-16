"""Shared pytest fixtures for the test suite.

Provides reusable fixtures for testing FastAPI endpoints and configurations.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Provide test settings with safe defaults.

    These settings use local/test values and should never connect to
    production services.

    Yields:
        Settings: Test configuration.
    """
    return Settings(
        environment="testing",
        debug=True,
        supabase_url="https://test.supabase.co",
        supabase_key="test_key",
        supabase_service_key="test_service_key",
        xai_api_key=None,
        use_local_llm=True,
        stripe_secret_key=None,
        cors_origins=["http://localhost:3000"],
        log_level="DEBUG",
    )


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient for endpoint testing.

    Creates a fresh FastAPI app instance and wraps it in a test client
    for making requests during tests.

    Returns:
        TestClient: Configured test client.
    """
    app = create_app()
    return TestClient(app)
