"""Reading API endpoints for tarot reading operations.

Provides endpoints for creating readings, listing spreads, and retrieving reading details.
"""

from datetime import datetime
from uuid import uuid4

import structlog
from fastapi import APIRouter, HTTPException, status

from app.core.llm.client import LLMFactory
from app.core.llm.prompts import PromptTemplates
from app.core.tarot.deck import TarotDeck
from app.core.tarot.spreads import SpreadLibrary
from app.schemas.reading import (
    CardInReading,
    ReadingRequest,
    ReadingResponse,
    SpreadPositionResponse,
    SpreadResponse,
    SpreadTypeEnum,
)

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api", tags=["readings"])


@router.post(
    "/reading", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED
)
async def create_reading(request: ReadingRequest) -> ReadingResponse:
    """Create a new tarot reading.

    Flow:
    1. Validate spread type exists
    2. Draw cards for the spread
    3. Build LLM prompt with cards
    4. Generate interpretation using LLM
    5. Return reading with cards and interpretation

    Args:
        request: ReadingRequest with question and spread_type

    Returns:
        ReadingResponse with cards and interpretation

    Raises:
        HTTPException 400: Invalid spread type
        HTTPException 503: LLM service error
    """
    try:
        # Get spread configuration
        spread = SpreadLibrary.get_spread(request.spread_type.value)
        if not spread:
            msg = f"Unknown spread type: {request.spread_type}"
            logger.error("invalid_spread_type", spread_type=request.spread_type)
            raise HTTPException(status_code=400, detail=msg)

        # Draw cards
        deck = TarotDeck()
        drawn_cards = deck.draw_with_reversals(spread.card_count)

        logger.info(
            "cards_drawn_for_reading",
            count=spread.card_count,
            spread_type=request.spread_type.value,
        )

        # Build prompt based on spread type
        if request.spread_type == SpreadTypeEnum.THREE_CARD:
            if len(drawn_cards) != 3:
                msg = "Three-card spread requires exactly 3 cards"
                raise HTTPException(status_code=500, detail=msg)

            user_prompt = PromptTemplates.get_three_card_prompt(
                question=request.question,
                past_card=drawn_cards[0],
                present_card=drawn_cards[1],
                future_card=drawn_cards[2],
                past_reversed=drawn_cards[0].get("is_reversed", False),
                present_reversed=drawn_cards[1].get("is_reversed", False),
                future_reversed=drawn_cards[2].get("is_reversed", False),
            )
        else:
            # Generic prompt for other spreads
            cards_info = ", ".join([f"{c.get('name', 'Unknown')}" for c in drawn_cards])
            user_prompt = f"""A seeker has drawn cards for reflection on their situation using the {spread.name} spread.

**Question**: {request.question}

**Cards drawn**: {cards_info}

Please provide a meaningful interpretation that honors each card's meaning and position in the spread. Speak directly to the querent with wisdom and warmth."""

        # Generate interpretation
        llm_client = LLMFactory.get_instance()
        interpretation = await llm_client.generate(
            system_prompt=PromptTemplates.SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        logger.info(
            "reading_interpretation_generated",
            spread_type=request.spread_type.value,
            interpretation_length=len(interpretation),
        )

        # Build response
        reading_id = str(uuid4())
        cards_response = []

        for i, card in enumerate(drawn_cards):
            position = spread.positions[i]
            card_response = CardInReading(
                id=card.get("id", "unknown"),
                name=card.get("name", "Unknown"),
                position=position.name,
                is_reversed=card.get("is_reversed", False),
                image_url=f"/cards/{card.get('image', 'unknown')}",
                number=card.get("number"),
                numeral=card.get("numeral"),
                keywords=card.get("keywords"),
                archetype=card.get("archetype"),
                hermetic_principle=card.get("hermetic_principle"),
                upright=card.get("upright"),
                reversed=card.get("reversed"),
            )
            cards_response.append(card_response)

        response = ReadingResponse(
            id=reading_id,
            question=request.question,
            spread_type=request.spread_type,
            cards=cards_response,
            interpretation=interpretation,
            created_at=datetime.now(),
        )

        logger.info("reading_created", reading_id=reading_id)
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "reading_creation_failed", error=str(e), exception_type=type(e).__name__
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to generate reading interpretation",
        ) from e


@router.get("/spreads", response_model=list[SpreadResponse])
async def list_spreads() -> list[SpreadResponse]:
    """Get all available tarot spreads.

    Returns a list of spread definitions with their positions and instructions,
    used by the frontend to populate spread selector.

    Returns:
        List of SpreadResponse objects
    """
    spreads = SpreadLibrary.get_all_spreads()
    responses = []

    for spread in spreads.values():
        positions = [
            SpreadPositionResponse(
                position=pos.position,
                name=pos.name,
                meaning=pos.meaning,
                guidance=pos.guidance,
            )
            for pos in spread.positions
        ]

        response = SpreadResponse(
            name=spread.name,
            spread_id=spread.spread_id,
            description=spread.description,
            card_count=spread.card_count,
            positions=positions,
            instructions=spread.instructions,
        )
        responses.append(response)

    logger.info("spreads_listed", count=len(responses))
    return responses
