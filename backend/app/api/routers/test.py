"""Test endpoints for development and debugging.

These endpoints are disabled in production and help verify
that core systems (LLM, deck, etc.) are working.
"""

from typing import Any

import structlog
from fastapi import APIRouter, HTTPException, status

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/test", tags=["test"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def test_health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict: Status message
    """
    return {"status": "healthy"}


@router.get("/deck")
async def test_deck() -> dict[str, Any]:
    """Test tarot deck loading and card drawing.

    Returns:
        dict: Sample cards from deck
    """
    try:
        from app.core.tarot.deck import TarotDeck

        deck = TarotDeck()
        cards = deck.draw(3)

        return {
            "status": "success",
            "total_cards": len(deck.all_cards),
            "sample_cards": [
                {"name": card["name"], "archetype": card.get("archetype", "")}
                for card in cards
            ],
        }
    except Exception as e:
        import traceback

        logger.error("deck_error", error=str(e), traceback=traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deck error: {str(e)}",
        ) from e


@router.get("/spreads")
async def test_spreads() -> dict[str, Any]:
    """List all available spreads.

    Returns:
        dict: Available spreads with details
    """
    from app.core.tarot.spreads import SpreadLibrary

    spreads = SpreadLibrary.get_all_spreads()

    return {
        "status": "success",
        "total_spreads": len(spreads),
        "spreads": [
            {
                "id": spread.spread_id,
                "name": spread.name,
                "card_count": spread.card_count,
                "description": spread.description,
            }
            for spread in spreads.values()
        ],
    }


@router.post("/llm")
async def test_llm(prompt: str = "What is the meaning of life?") -> dict[str, Any]:
    """Test LLM integration.

    Args:
        prompt: Test prompt to send to LLM

    Returns:
        dict: LLM response and metadata
    """
    try:
        from app.config import get_settings
        from app.core.llm.client import LLMFactory

        settings = get_settings()
        client = LLMFactory.create(
            use_local=settings.use_local_llm,
            ollama_base_url=settings.ollama_base_url,
            grok_api_key=settings.xai_api_key,
        )

        # Simple test
        response = await client.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt=prompt,
        )

        logger.info("llm_test_success", response_length=len(response))

        return {
            "status": "success",
            "provider": "ollama" if settings.use_local_llm else "grok",
            "prompt": prompt,
            "response": response,
        }

    except Exception as e:
        logger.error("llm_test_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM error: {str(e)}",
        ) from e


@router.get("/supabase")
async def test_supabase() -> dict[str, Any]:
    """Test Supabase connection.

    Returns:
        dict: Connection status for auth and database
    """
    try:
        from supabase import create_client

        from app.config import get_settings

        settings = get_settings()
        client = create_client(settings.supabase_url, settings.supabase_key)

        results: dict[str, Any] = {"status": "success", "checks": {}}

        # Test auth connection
        try:
            client.auth.get_session()
            results["checks"]["auth"] = "connected"
        except Exception as e:
            results["checks"]["auth"] = f"error: {str(e)[:50]}"

        # Test database connection
        try:
            response = client.table("readings").select("id").limit(1).execute()
            results["checks"]["database"] = "connected"
            results["checks"]["readings_table"] = f"{len(response.data)} rows"
        except Exception as e:
            error_str = str(e)
            if "does not exist" in error_str:
                results["checks"]["database"] = "connected (table not created)"
            else:
                results["checks"]["database"] = f"error: {error_str[:50]}"

        logger.info("supabase_test_success", checks=results["checks"])
        return results

    except Exception as e:
        logger.error("supabase_test_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Supabase error: {str(e)}",
        ) from e


@router.post("/reading")
async def test_reading(
    question: str = "What do I need to know right now?",
) -> dict[str, Any]:
    """Test complete reading flow: draw cards, interpret with LLM.

    Args:
        question: The querent's question

    Returns:
        dict: Complete reading with cards and interpretation
    """
    try:
        from app.config import get_settings
        from app.core.llm.client import LLMFactory
        from app.core.llm.prompts import PromptTemplates
        from app.core.tarot.deck import TarotDeck
        from app.core.tarot.spreads import SpreadLibrary

        settings = get_settings()

        # Draw cards
        deck = TarotDeck()
        cards = deck.draw_with_reversals(3)

        # Get spread info
        spread = SpreadLibrary.three_card()

        # Prepare LLM prompt
        past_card = cards[0]
        present_card = cards[1]
        future_card = cards[2]

        prompt = PromptTemplates.get_three_card_prompt(
            question=question,
            past_card=past_card,
            present_card=present_card,
            future_card=future_card,
            past_reversed=past_card.get("is_reversed", False),
            present_reversed=present_card.get("is_reversed", False),
            future_reversed=future_card.get("is_reversed", False),
        )

        # Get LLM interpretation
        client = LLMFactory.create(
            use_local=settings.use_local_llm,
            ollama_base_url=settings.ollama_base_url,
            grok_api_key=settings.xai_api_key,
        )

        interpretation = await client.generate(
            system_prompt=PromptTemplates.SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        logger.info(
            "reading_test_success",
            question=question,
            cards=[c["name"] for c in cards],
        )

        return {
            "status": "success",
            "question": question,
            "spread": {
                "name": spread.name,
                "positions": [
                    {"position": p.position, "name": p.name} for p in spread.positions
                ],
            },
            "cards": [
                {
                    "position": i,
                    "name": card["name"],
                    "archetype": card.get("archetype", ""),
                    "reversed": card.get("is_reversed", False),
                }
                for i, card in enumerate(cards)
            ],
            "interpretation": interpretation,
        }

    except Exception as e:
        logger.error("reading_test_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reading error: {str(e)}",
        ) from e
