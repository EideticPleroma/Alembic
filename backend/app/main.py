"""Alembic FastAPI application.

Main entry point for the backend API. Sets up the FastAPI app with
middleware, routers, and lifespan event handlers.
"""

from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api.routers import health
from app.config import Settings, get_settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> Any:
    """Manage app startup and shutdown.

    Args:
        _app: FastAPI application instance.

    Yields:
        Control back to FastAPI after startup.
    """
    # Startup
    settings = get_settings()
    logger.info(
        "startup",
        environment=settings.environment,
        debug=settings.debug,
    )

    yield

    # Shutdown
    logger.info("shutdown", environment=settings.environment)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    try:
        settings = get_settings()
    except ValidationError as e:
        logger.warning("settings_load_failed", error=str(e), using_defaults=True)
        settings = Settings(
            supabase_url="https://default.supabase.co",
            supabase_key="default",
            supabase_service_key="default",
        )

    app = FastAPI(
        title="Alembic",
        description="AI-powered Hermetic tarot reading application",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router)

    return app


# Application instance
app = create_app()
