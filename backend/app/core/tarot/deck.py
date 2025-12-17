"""Tarot deck management and card drawing logic.

This module provides the Tarot Deck class for managing the 78-card deck,
drawing random cards, and managing spread positions.
"""

import json
import random
import secrets
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class TarotDeck:
    """Represents the complete 78-card Tarot deck with cryptographic drawing."""

    def __init__(self) -> None:
        """Initialize the deck by loading cards from JSON data file."""
        self.cards_file = Path(__file__).parent / "data" / "cards.json"
        self.deck_data = self._load_cards()
        self.all_cards = self._build_card_list()

    def _load_cards(self) -> dict[str, Any]:
        """Load card data from JSON file.

        Returns:
            dict: Parsed card data including major and minor arcana.

        Raises:
            FileNotFoundError: If cards.json cannot be found.
        """
        if not self.cards_file.exists():
            msg = f"Cards file not found at {self.cards_file}"
            raise FileNotFoundError(msg)

        with open(self.cards_file) as f:
            return json.load(f)  # type: ignore[no-any-return]

    def _build_card_list(self) -> list[dict[str, Any]]:
        """Build a flat list of all cards from deck data.

        Returns:
            list: All 78 cards with their metadata.
        """
        cards: list[dict[str, Any]] = []
        major = self.deck_data.get("major_arcana", [])
        minor = self.deck_data.get("minor_arcana", [])
        cards.extend(major)
        cards.extend(minor)
        return cards

    def draw(self, count: int = 1) -> list[dict[str, Any]]:
        """Draw random cards using cryptographic randomness.

        Uses secrets.choice for cryptographically secure random selection,
        suitable for divination where fairness matters psychologically.

        Args:
            count: Number of cards to draw (default 1)

        Returns:
            list: List of drawn cards in order

        Raises:
            ValueError: If count exceeds 78 or is less than 1
        """
        if count < 1 or count > 78:
            msg = f"Cannot draw {count} cards from 78-card deck"
            raise ValueError(msg)

        drawn = []
        available = self.all_cards.copy()

        for _ in range(count):
            card = secrets.choice(available)
            drawn.append(card)
            available.remove(card)

        logger.info("cards_drawn", count=count, cards=[c["name"] for c in drawn])
        return drawn

    def draw_with_reversals(self, count: int = 1) -> list[dict[str, Any]]:
        """Draw cards and randomly assign reversals.

        Each card has a 50% chance of being reversed (meaning interpreted
        in shadow/negative aspect).

        Args:
            count: Number of cards to draw

        Returns:
            list: Cards with 'reversed' boolean flag added
        """
        cards = self.draw(count)

        for card in cards:
            card["is_reversed"] = random.choice([True, False])

        return cards

    def get_card_by_id(self, card_id: str) -> dict[str, Any] | None:
        """Retrieve a specific card by ID.

        Args:
            card_id: Card ID (e.g., "major_00", "minor_cups_01")

        Returns:
            Card data if found, None otherwise
        """
        for card in self.all_cards:
            if card["id"] == card_id:
                return card
        return None

    def get_major_arcana(self) -> list[dict[str, Any]]:
        """Get all major arcana cards.

        Returns:
            list: All 22 major arcana cards
        """
        result: list[dict[str, Any]] = self.deck_data.get("major_arcana", [])
        return result

    def get_minor_arcana(self) -> list[dict[str, Any]]:
        """Get all minor arcana cards.

        Returns:
            list: All 56 minor arcana cards
        """
        result: list[dict[str, Any]] = self.deck_data.get("minor_arcana", [])
        return result
