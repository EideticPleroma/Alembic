"""Schemas for reading creation and retrieval.

Defines Pydantic models for request/response contracts matching the API design.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SpreadTypeEnum(str, Enum):
    """Valid spread types."""

    ONE_CARD = "one_card"
    THREE_CARD = "three_card"
    SHADOW_WORK = "shadow_work"
    CELTIC_CROSS = "celtic_cross"


class ReadingRequest(BaseModel):
    """Request to create a new reading.

    Attributes:
        question: User's question (1-1000 characters)
        spread_type: Type of spread to use
    """

    question: str = Field(..., min_length=1, max_length=1000)
    spread_type: SpreadTypeEnum


class CardInReading(BaseModel):
    """Card data within a reading response.

    Attributes:
        id: Card ID (e.g., "major_00", "cups_ace")
        name: Card name (e.g., "The Fool", "Ace of Cups")
        position: Position in spread (e.g., "Past", "Present")
        is_reversed: Whether card is reversed (shadow/blocked energy)
        image_url: URL to card image
        number: Card number (for arcana cards)
        numeral: Roman numeral (for major arcana)
        keywords: List of keywords associated with the card
        archetype: Jungian archetype name
        hermetic_principle: Associated hermetic principle
        upright: Meaning when upright
        reversed: Meaning when reversed
    """

    id: str
    name: str
    position: str
    is_reversed: bool
    image_url: str
    number: int | None = None
    numeral: str | None = None
    keywords: list[str] | None = None
    archetype: str | None = None
    hermetic_principle: str | None = None
    upright: str | None = None
    reversed: str | None = None


class ReadingResponse(BaseModel):
    """Response from creating a reading.

    Attributes:
        id: Reading UUID
        question: The user's question
        spread_type: Type of spread used
        cards: Cards drawn for this reading
        interpretation: LLM-generated interpretation
        created_at: Timestamp of reading creation
    """

    id: str
    question: str
    spread_type: SpreadTypeEnum
    cards: list[CardInReading]
    interpretation: str
    created_at: datetime


class ReadingListItem(BaseModel):
    """Summary item for readings list.

    Attributes:
        id: Reading UUID
        question: The user's question
        spread_type: Type of spread used
        created_at: Timestamp of reading creation
    """

    id: str
    question: str
    spread_type: SpreadTypeEnum
    created_at: datetime


class ReadingListResponse(BaseModel):
    """Paginated list of readings.

    Attributes:
        readings: List of reading summaries
        total: Total number of readings
        limit: Max results per page
        offset: Pagination offset
    """

    readings: list[ReadingListItem]
    total: int
    limit: int
    offset: int


class SpreadPositionResponse(BaseModel):
    """Position definition within a spread.

    Attributes:
        position: Position index (0-based)
        name: Position name (e.g., "Past", "Present")
        meaning: What this position represents
        guidance: Reflection question for this position
    """

    position: int
    name: str
    meaning: str
    guidance: str


class SpreadResponse(BaseModel):
    """Available spread definition.

    Attributes:
        name: Spread name (e.g., "Three Card")
        spread_id: Unique identifier (e.g., "three_card")
        description: What this spread is for
        card_count: How many cards are drawn
        positions: List of position definitions
        instructions: How to perform this spread
    """

    name: str
    spread_id: str
    description: str
    card_count: int
    positions: list[SpreadPositionResponse]
    instructions: str
