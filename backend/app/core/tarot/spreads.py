"""Tarot spread definitions and management.

Spreads define the structure and meaning of card positions for readings.
This module provides common spreads and a framework for creating custom ones.
"""

from dataclasses import dataclass

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class SpreadPosition:
    """Represents a position in a tarot spread."""

    position: int
    name: str
    meaning: str
    guidance: str


@dataclass
class Spread:
    """Represents a complete tarot spread structure."""

    name: str
    spread_id: str
    description: str
    card_count: int
    positions: list[SpreadPosition]
    instructions: str


class SpreadLibrary:
    """Collection of tarot spreads available in Alembic."""

    @staticmethod
    def three_card() -> Spread:
        """The foundational three-card spread: Past, Present, Future.

        This is the most accessible spread for newcomers and the default
        in Alembic's free tier. It provides sufficient depth for meaningful
        reflection on any life situation.

        Returns:
            Spread: Three-card spread configuration
        """
        return Spread(
            name="Three Card",
            spread_id="three_card",
            description="Past, Present, Future - The foundational spread for any situation",
            card_count=3,
            positions=[
                SpreadPosition(
                    position=0,
                    name="Past",
                    meaning="The influences and experiences that brought you here",
                    guidance="What foundation or cycle are you completing?",
                ),
                SpreadPosition(
                    position=1,
                    name="Present",
                    meaning="The current energies and circumstances",
                    guidance="What is the true nature of your situation right now?",
                ),
                SpreadPosition(
                    position=2,
                    name="Future",
                    meaning="The potential outcome and energies ahead",
                    guidance="What is trying to emerge? What is the next chapter?",
                ),
            ],
            instructions="Shuffle and draw three cards. Lay them left to right.",
        )

    @staticmethod
    def celtic_cross() -> Spread:
        """The Celtic Cross - a comprehensive 10-card spread.

        This classic spread provides nuanced insight into a situation,
        including hidden influences and potential outcomes.

        Returns:
            Spread: Celtic Cross spread configuration
        """
        return Spread(
            name="Celtic Cross",
            spread_id="celtic_cross",
            description="A comprehensive 10-card spread exploring all dimensions of a situation",
            card_count=10,
            positions=[
                SpreadPosition(
                    position=0,
                    name="Significator",
                    meaning="The heart of the matter",
                    guidance="What is this really about?",
                ),
                SpreadPosition(
                    position=1,
                    name="Challenge",
                    meaning="The obstacle or influence to navigate",
                    guidance="What is the true challenge here?",
                ),
                SpreadPosition(
                    position=2,
                    name="Root",
                    meaning="The foundation or origin of the situation",
                    guidance="Where does this come from?",
                ),
                SpreadPosition(
                    position=3,
                    name="Recent Past",
                    meaning="Recent influences that shaped the present",
                    guidance="What just happened?",
                ),
                SpreadPosition(
                    position=4,
                    name="Possible Outcome",
                    meaning="Where things are naturally heading",
                    guidance="What is the likely path?",
                ),
                SpreadPosition(
                    position=5,
                    name="Near Future",
                    meaning="Energies coming into play soon",
                    guidance="What is emerging?",
                ),
                SpreadPosition(
                    position=6,
                    name="Your Attitude",
                    meaning="Your role and perspective in this",
                    guidance="How are you approaching this?",
                ),
                SpreadPosition(
                    position=7,
                    name="Others' Influence",
                    meaning="How others or external forces affect this",
                    guidance="What are others bringing?",
                ),
                SpreadPosition(
                    position=8,
                    name="Hopes/Fears",
                    meaning="Your deeper desires or anxieties",
                    guidance="What do you really want? What scares you?",
                ),
                SpreadPosition(
                    position=9,
                    name="Outcome",
                    meaning="The ultimate resolution or lesson",
                    guidance="What is being revealed?",
                ),
            ],
            instructions="Shuffle and draw 10 cards, placing them in the Celtic Cross pattern.",
        )

    @staticmethod
    def shadow_work() -> Spread:
        """Shadow Work spread - explore denied aspects of self.

        This spread is designed for deep psychological work, exploring
        the shadow self according to Jungian principles.

        Returns:
            Spread: Shadow Work spread configuration
        """
        return Spread(
            name="Shadow Work",
            spread_id="shadow_work",
            description="A 4-card spread for integrating shadow aspects and unconscious patterns",
            card_count=4,
            positions=[
                SpreadPosition(
                    position=0,
                    name="What I Deny",
                    meaning="The aspect of myself I reject or don't acknowledge",
                    guidance="What quality do I judge in others that I possess?",
                ),
                SpreadPosition(
                    position=1,
                    name="Why I Hide It",
                    meaning="The fear or belief that causes repression",
                    guidance="What am I afraid will happen if I claim this?",
                ),
                SpreadPosition(
                    position=2,
                    name="Its Gift",
                    meaning="The positive potential of this shadow aspect",
                    guidance="How could this power serve me if integrated?",
                ),
                SpreadPosition(
                    position=3,
                    name="Integration Path",
                    meaning="How to bring this aspect into consciousness",
                    guidance="What action opens me to wholeness?",
                ),
            ],
            instructions="Shuffle and draw 4 cards for deep shadow work. Move slowly with this spread.",
        )

    @staticmethod
    def one_card() -> Spread:
        """One Card Oracle - a single powerful card for reflection.

        Returns:
            Spread: Single card spread configuration
        """
        return Spread(
            name="One Card",
            spread_id="one_card",
            description="A single card for daily guidance or specific focus",
            card_count=1,
            positions=[
                SpreadPosition(
                    position=0,
                    name="Message",
                    meaning="The card's message for you today",
                    guidance="What is this card showing you?",
                ),
            ],
            instructions="Draw one card and sit with its message.",
        )

    @staticmethod
    def get_all_spreads() -> dict[str, Spread]:
        """Get all available spreads as a dictionary.

        Returns:
            dict: All spreads keyed by spread_id
        """
        spreads = [
            SpreadLibrary.one_card(),
            SpreadLibrary.three_card(),
            SpreadLibrary.celtic_cross(),
            SpreadLibrary.shadow_work(),
        ]
        return {spread.spread_id: spread for spread in spreads}

    @staticmethod
    def get_spread(spread_id: str) -> Spread | None:
        """Retrieve a specific spread by ID.

        Args:
            spread_id: The spread identifier

        Returns:
            Spread if found, None otherwise
        """
        all_spreads = SpreadLibrary.get_all_spreads()
        return all_spreads.get(spread_id)
