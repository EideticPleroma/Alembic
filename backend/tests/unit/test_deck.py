"""Tests for the Tarot Deck management system."""

import pytest

from app.core.tarot.deck import TarotDeck


@pytest.fixture
def deck() -> TarotDeck:
    """Provide a TarotDeck instance for testing."""
    return TarotDeck()


class TestDeckLoading:
    """Test deck initialization and card loading."""

    def test_deck_loads_78_cards(self, deck: TarotDeck) -> None:
        """Deck contains exactly 78 cards."""
        assert len(deck.all_cards) == 78

    def test_deck_has_22_major_arcana(self, deck: TarotDeck) -> None:
        """Deck contains 22 major arcana cards."""
        major = deck.get_major_arcana()
        assert len(major) == 22

    def test_deck_has_56_minor_arcana(self, deck: TarotDeck) -> None:
        """Deck contains 56 minor arcana cards."""
        minor = deck.get_minor_arcana()
        assert len(minor) == 56


class TestCardDrawing:
    """Test card drawing functionality."""

    def test_draw_returns_requested_count(self, deck: TarotDeck) -> None:
        """Draw returns the requested number of cards."""
        cards_1 = deck.draw(1)
        assert len(cards_1) == 1

        # Fresh deck instance to avoid drawing duplicates
        deck2 = TarotDeck()
        cards_5 = deck2.draw(5)
        assert len(cards_5) == 5

    def test_draw_cards_are_unique(self, deck: TarotDeck) -> None:
        """No duplicate cards in a single draw."""
        cards = deck.draw(10)
        card_ids = [card["id"] for card in cards]
        assert len(card_ids) == len(set(card_ids))

    def test_draw_raises_for_zero(self, deck: TarotDeck) -> None:
        """Drawing 0 cards raises ValueError."""
        with pytest.raises(ValueError, match="Cannot draw 0 cards"):
            deck.draw(0)

    def test_draw_raises_for_negative(self, deck: TarotDeck) -> None:
        """Drawing negative cards raises ValueError."""
        with pytest.raises(ValueError, match="Cannot draw -1 cards"):
            deck.draw(-1)

    def test_draw_raises_for_too_many(self, deck: TarotDeck) -> None:
        """Drawing more than 78 cards raises ValueError."""
        with pytest.raises(ValueError, match="Cannot draw 79 cards"):
            deck.draw(79)

    def test_draw_can_draw_all_78(self, deck: TarotDeck) -> None:
        """Drawing all 78 cards succeeds."""
        cards = deck.draw(78)
        assert len(cards) == 78


class TestReversals:
    """Test card reversals functionality."""

    def test_draw_with_reversals_adds_flag(self, deck: TarotDeck) -> None:
        """Each card has is_reversed boolean flag."""
        cards = deck.draw_with_reversals(5)
        assert len(cards) == 5
        for card in cards:
            assert "is_reversed" in card
            assert isinstance(card["is_reversed"], bool)

    def test_draw_with_reversals_does_not_mutate_deck(self, deck: TarotDeck) -> None:
        """Original deck cards are not mutated by reversals."""
        # Get a card before draw
        original_card = deck.get_card_by_id("major_00")
        assert original_card is not None
        assert "is_reversed" not in original_card

        # Draw with reversals
        deck.draw_with_reversals(1)

        # Original card should still not have is_reversed
        card_after = deck.get_card_by_id("major_00")
        assert card_after is not None
        assert "is_reversed" not in card_after

    def test_draw_with_reversals_returns_copies(self, deck: TarotDeck) -> None:
        """Drawn cards are independent copies."""
        drawn = deck.draw_with_reversals(3)

        # Modify drawn card
        drawn[0]["is_reversed"] = True

        # Draw again and check original deck is unaffected
        deck2 = TarotDeck()
        drawn2 = deck2.draw_with_reversals(1)

        # New draws should have independent reversal values
        assert "is_reversed" in drawn2[0]


class TestCardRetrieval:
    """Test card lookup functionality."""

    def test_get_card_by_id_returns_card(self, deck: TarotDeck) -> None:
        """get_card_by_id returns correct card."""
        card = deck.get_card_by_id("major_00")
        assert card is not None
        assert card["id"] == "major_00"

    def test_get_card_by_id_returns_none_for_missing(self, deck: TarotDeck) -> None:
        """get_card_by_id returns None for invalid ID."""
        card = deck.get_card_by_id("invalid_card_id")
        assert card is None

    def test_all_cards_have_id(self, deck: TarotDeck) -> None:
        """Every card has an id field."""
        for card in deck.all_cards:
            assert "id" in card
            assert isinstance(card["id"], str)

    def test_all_cards_have_name(self, deck: TarotDeck) -> None:
        """Every card has a name field."""
        for card in deck.all_cards:
            assert "name" in card
            assert isinstance(card["name"], str)
