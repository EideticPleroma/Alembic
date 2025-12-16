"""Health check endpoint.

Provides a simple health check to verify the API is running.
In Phase 0, reports basic status. Service-specific checks (database, LLM, etc.)
are added in subsequent phases.
"""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, Any]:
    """Check API health status.

    Returns a JSON response with the current health status and timestamp.
    In Phase 0, this is a basic check. Database, LLM, and Stripe checks
    will be added when those services are integrated.

    Returns:
        dict: Health status with checks and timestamp.
    """
    return {
        "status": "healthy",
        "checks": {
            "database": None,
            "llm": None,
            "stripe": None,
        },
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
