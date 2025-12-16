"""Dependency injection for API endpoints.

Provides functions that FastAPI can inject as dependencies.
Follows the FastAPI Depends pattern for clean endpoint signatures.
"""

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings


def get_settings_dep() -> Settings:
    """Get application settings.

    This dependency provides access to application configuration
    throughout the API endpoints.

    Returns:
        Settings: Application configuration.
    """
    return get_settings()


SettingsDep = Annotated[Settings, Depends(get_settings_dep)]
