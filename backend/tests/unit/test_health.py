"""Tests for the health check endpoint."""

from fastapi.testclient import TestClient


def test_health_check_returns_200(client: TestClient) -> None:
    """Health endpoint returns 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_has_status_field(client: TestClient) -> None:
    """Health response includes 'status' field."""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_health_check_has_checks_field(client: TestClient) -> None:
    """Health response includes 'checks' field with service statuses."""
    response = client.get("/health")
    data = response.json()
    assert "checks" in data
    assert isinstance(data["checks"], dict)


def test_health_check_has_database_check(client: TestClient) -> None:
    """Health response includes database check status."""
    response = client.get("/health")
    data = response.json()
    assert "database" in data["checks"]


def test_health_check_has_llm_check(client: TestClient) -> None:
    """Health response includes LLM check status."""
    response = client.get("/health")
    data = response.json()
    assert "llm" in data["checks"]


def test_health_check_has_stripe_check(client: TestClient) -> None:
    """Health response includes Stripe check status."""
    response = client.get("/health")
    data = response.json()
    assert "stripe" in data["checks"]


def test_health_check_has_timestamp(client: TestClient) -> None:
    """Health response includes ISO 8601 timestamp."""
    response = client.get("/health")
    data = response.json()
    assert "timestamp" in data
    assert "T" in data["timestamp"]
    assert "Z" in data["timestamp"]


def test_health_check_timestamp_is_valid_iso8601(client: TestClient) -> None:
    """Health response timestamp is valid ISO 8601 format."""
    from datetime import datetime

    response = client.get("/health")
    data = response.json()
    timestamp = data["timestamp"]

    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        valid = True
    except ValueError:
        valid = False

    assert valid, f"Timestamp {timestamp} is not valid ISO 8601"
