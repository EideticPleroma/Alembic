"""Tests for the reading API endpoints."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.core.llm.client import LLMResponse


@pytest.fixture
def mock_llm_generate():  # type: ignore[no-untyped-def]
    """Mock LLM generation to avoid real API calls."""

    async def mock_generate(
        self: object, system_prompt: str, user_prompt: str
    ) -> LLMResponse:
        _ = (self, system_prompt, user_prompt)
        return LLMResponse(
            content="This is a mock interpretation generated for testing purposes.",
            model="mock-model",
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            cost_usd=0.0,
        )

    return mock_generate


class TestCreateReading:
    """Test POST /api/reading endpoint."""

    def test_create_reading_returns_201(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Successful reading creation returns 201 status."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "What should I focus on today?",
                    "spread_type": "three_card",
                },
            )
            assert response.status_code == 201

    def test_create_reading_returns_cards(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Reading response includes cards array."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "What guidance do I need?",
                    "spread_type": "three_card",
                },
            )
            data = response.json()
            assert "cards" in data
            assert isinstance(data["cards"], list)
            assert len(data["cards"]) == 3

    def test_create_reading_returns_interpretation(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Reading response includes interpretation."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "What message do the cards have?",
                    "spread_type": "three_card",
                },
            )
            data = response.json()
            assert "interpretation" in data
            assert len(data["interpretation"]) > 0

    def test_create_reading_returns_id(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Reading response includes UUID."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "What is my next step?",
                    "spread_type": "three_card",
                },
            )
            data = response.json()
            assert "id" in data
            assert len(data["id"]) > 0

    def test_create_reading_validates_question_empty(self, client: TestClient) -> None:
        """Empty question is rejected."""
        response = client.post(
            "/api/reading",
            json={"question": "", "spread_type": "three_card"},
        )
        assert response.status_code == 422

    def test_create_reading_validates_question_too_long(
        self, client: TestClient
    ) -> None:
        """Question longer than 1000 characters is rejected."""
        long_question = "x" * 1001
        response = client.post(
            "/api/reading",
            json={"question": long_question, "spread_type": "three_card"},
        )
        assert response.status_code == 422

    def test_create_reading_validates_spread_type(self, client: TestClient) -> None:
        """Invalid spread type is rejected."""
        response = client.post(
            "/api/reading",
            json={
                "question": "What should I know?",
                "spread_type": "invalid_spread",
            },
        )
        assert response.status_code == 422

    def test_create_reading_three_card_has_positions(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Three-card spread has Past/Present/Future positions."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "What is my situation?",
                    "spread_type": "three_card",
                },
            )
            data = response.json()
            positions = [card["position"] for card in data["cards"]]
            assert "Past" in positions
            assert "Present" in positions
            assert "Future" in positions

    def test_create_reading_includes_created_at(
        self, client: TestClient, mock_llm_generate: object
    ) -> None:
        """Response includes created_at timestamp."""
        with patch("app.core.llm.client.OllamaClient.generate", mock_llm_generate):
            response = client.post(
                "/api/reading",
                json={
                    "question": "When was this created?",
                    "spread_type": "three_card",
                },
            )
            data = response.json()
            assert "created_at" in data
            assert "T" in data["created_at"]


class TestListSpreads:
    """Test GET /api/spreads endpoint."""

    def test_list_spreads_returns_200(self, client: TestClient) -> None:
        """List spreads returns 200 OK."""
        response = client.get("/api/spreads")
        assert response.status_code == 200

    def test_list_spreads_returns_array(self, client: TestClient) -> None:
        """List spreads returns an array."""
        response = client.get("/api/spreads")
        data = response.json()
        assert isinstance(data, list)

    def test_list_spreads_returns_all_spreads(self, client: TestClient) -> None:
        """List spreads returns all 4 available spreads."""
        response = client.get("/api/spreads")
        data = response.json()
        assert len(data) == 4

    def test_list_spreads_includes_three_card(self, client: TestClient) -> None:
        """List includes three_card spread."""
        response = client.get("/api/spreads")
        data = response.json()
        spread_ids = [spread["spread_id"] for spread in data]
        assert "three_card" in spread_ids

    def test_list_spreads_includes_positions(self, client: TestClient) -> None:
        """Each spread has position definitions."""
        response = client.get("/api/spreads")
        data = response.json()
        for spread in data:
            assert "positions" in spread
            assert isinstance(spread["positions"], list)
            assert len(spread["positions"]) > 0
            for position in spread["positions"]:
                assert "name" in position
                assert "meaning" in position
                assert "guidance" in position

    def test_list_spreads_includes_instructions(self, client: TestClient) -> None:
        """Each spread has instructions."""
        response = client.get("/api/spreads")
        data = response.json()
        for spread in data:
            assert "instructions" in spread
            assert isinstance(spread["instructions"], str)

    def test_list_spreads_includes_card_count(self, client: TestClient) -> None:
        """Each spread includes card count."""
        response = client.get("/api/spreads")
        data = response.json()
        for spread in data:
            assert "card_count" in spread
            assert spread["card_count"] > 0

    def test_spreads_have_correct_card_counts(self, client: TestClient) -> None:
        """Spreads have expected card counts."""
        response = client.get("/api/spreads")
        data = response.json()
        spread_counts = {spread["spread_id"]: spread["card_count"] for spread in data}
        assert spread_counts.get("one_card") == 1
        assert spread_counts.get("three_card") == 3
        assert spread_counts.get("shadow_work") == 4
        assert spread_counts.get("celtic_cross") == 10
