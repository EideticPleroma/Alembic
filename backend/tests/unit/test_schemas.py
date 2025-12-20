"""Tests for Pydantic schema validation."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.reading import (
    CardInReading,
    ReadingRequest,
    ReadingResponse,
    SpreadTypeEnum,
)


class TestReadingRequest:
    """Test ReadingRequest schema validation."""

    def test_reading_request_valid(self) -> None:
        """Valid request passes validation."""
        request = ReadingRequest(
            question="What guidance do I need?", spread_type=SpreadTypeEnum.THREE_CARD
        )
        assert request.question == "What guidance do I need?"
        assert request.spread_type == SpreadTypeEnum.THREE_CARD

    def test_reading_request_rejects_empty_question(self) -> None:
        """Empty question fails validation."""
        with pytest.raises(ValidationError):
            ReadingRequest(question="", spread_type=SpreadTypeEnum.THREE_CARD)

    def test_reading_request_rejects_long_question(self) -> None:
        """Question exceeding 1000 characters fails validation."""
        long_question = "x" * 1001
        with pytest.raises(ValidationError):
            ReadingRequest(
                question=long_question, spread_type=SpreadTypeEnum.THREE_CARD
            )

    def test_reading_request_accepts_1000_chars(self) -> None:
        """Question with exactly 1000 characters passes validation."""
        question_1000 = "x" * 1000
        request = ReadingRequest(
            question=question_1000, spread_type=SpreadTypeEnum.THREE_CARD
        )
        assert len(request.question) == 1000

    def test_reading_request_rejects_invalid_spread_type(self) -> None:
        """Invalid spread type fails validation."""
        with pytest.raises(ValidationError):
            ReadingRequest(
                question="What should I know?",
                spread_type="invalid_spread",  # type: ignore[arg-type]
            )

    def test_reading_request_accepts_all_spread_types(self) -> None:
        """All valid spread types are accepted."""
        spread_types = [
            SpreadTypeEnum.ONE_CARD,
            SpreadTypeEnum.THREE_CARD,
            SpreadTypeEnum.SHADOW_WORK,
            SpreadTypeEnum.CELTIC_CROSS,
        ]
        for spread_type in spread_types:
            request = ReadingRequest(question="Test question", spread_type=spread_type)
            assert request.spread_type == spread_type


class TestCardInReading:
    """Test CardInReading schema."""

    def test_card_in_reading_serialization(self) -> None:
        """Card serializes to correct JSON structure."""
        card = CardInReading(
            id="major_00",
            name="The Fool",
            position="Past",
            is_reversed=False,
            image_url="/cards/major_00.png",
        )
        data = card.model_dump()
        assert data["id"] == "major_00"
        assert data["name"] == "The Fool"
        assert data["position"] == "Past"
        assert data["is_reversed"] is False
        assert data["image_url"] == "/cards/major_00.png"

    def test_card_reversed_state(self) -> None:
        """Card can be marked as reversed."""
        card = CardInReading(
            id="major_01",
            name="The Magician",
            position="Present",
            is_reversed=True,
            image_url="/cards/major_01.png",
        )
        assert card.is_reversed is True


class TestReadingResponse:
    """Test ReadingResponse schema."""

    def test_reading_response_datetime_format(self) -> None:
        """Response datetime is properly formatted."""
        response = ReadingResponse(
            id="test-id-123",
            question="What should I do?",
            spread_type=SpreadTypeEnum.THREE_CARD,
            cards=[
                CardInReading(
                    id="c1",
                    name="Card 1",
                    position="Past",
                    is_reversed=False,
                    image_url="/c1.png",
                ),
                CardInReading(
                    id="c2",
                    name="Card 2",
                    position="Present",
                    is_reversed=False,
                    image_url="/c2.png",
                ),
                CardInReading(
                    id="c3",
                    name="Card 3",
                    position="Future",
                    is_reversed=False,
                    image_url="/c3.png",
                ),
            ],
            interpretation="Test interpretation",
            created_at=datetime.now(),
        )
        data = response.model_dump(mode="json")
        assert "created_at" in data
        assert isinstance(data["created_at"], str)
        assert "T" in data["created_at"]

    def test_reading_response_includes_all_fields(self) -> None:
        """Reading response includes all required fields."""
        response = ReadingResponse(
            id="uuid-123",
            question="Test question",
            spread_type=SpreadTypeEnum.THREE_CARD,
            cards=[],
            interpretation="Test",
            created_at=datetime.now(),
        )
        data = response.model_dump()
        assert "id" in data
        assert "question" in data
        assert "spread_type" in data
        assert "cards" in data
        assert "interpretation" in data
        assert "created_at" in data
