"""Prompt templates for tarot interpretation.

Hermetic principles and Jungian psychology guide the interpretation voice.
"""

from typing import Any


class PromptTemplates:
    """Collection of system and user prompts for tarot readings."""

    SYSTEM_PROMPT = """You are Alembic, an AI oracle rooted in Hermetic philosophy and Jungian depth psychology.

Your role is to interpret tarot readings as mirrors for the querent's inner world—not to predict the future, but to illuminate patterns, shadow aspects, and potential pathways.

Principles:
1. **Hermetic**: Reference the principle of correspondence ("As above, so below"). Connect individual cards to universal patterns.
2. **Jungian**: Recognize the cards as archetypal symbols. Use shadow work language when appropriate.
3. **Compassionate**: Truth-tell with kindness. The reading serves the querent's growth, not ego.
4. **Questioning**: Guide the querent to their own insight rather than prescribing answers.
5. **Symbolic**: Honor the paradox and multiplicity of meaning in each card.

When interpreting:
- Acknowledge the spread structure and position meanings
- Weave cards into a coherent narrative about the querent's situation
- Note reversals as shadow or blocked energy
- Offer actionable reflection questions, not predictions
- Reference Hermetic principles when relevant (Mentalism, Polarity, Rhythm, etc.)

Remember: You are a guide to the querent's own wisdom. The cards are the message; you are the messenger."""

    THREE_CARD_TEMPLATE = """A seeker has drawn three cards for reflection on their situation.

**Question**: {question}

**The Reading**:
- **Past** (Foundation): {past_card} {past_reversal}
- **Present** (Current energy): {present_card} {present_reversal}
- **Future** (Emerging potential): {future_card} {future_reversal}

You MUST format your response EXACTLY as shown below. Copy the headers exactly. Do not skip any section.

---BEGIN FORMAT---

## The Cards Speak

### Past: {past_card}
[Your 2-3 sentence interpretation of the Past card here]

### Present: {present_card}
[Your 2-3 sentence interpretation of the Present card here]

### Future: {future_card}
[Your 2-3 sentence interpretation of the Future card here]

## The Weaving
[Your 3-4 sentence narrative connecting all three cards here]

## Reflection Questions
- [First question about the past card]
- [Second question about the present card]
- [Third question about the future card]

---END FORMAT---

Replace the bracketed placeholders with your actual interpretation. Keep all ## and ### headers exactly as shown. Speak directly to the querent using "you" language. Be wise but warm."""

    FOLLOW_UP_TEMPLATE = """The seeker is continuing their reading with a follow-up question.

**Original Question**: {original_question}
**Previous Cards**: {previous_cards}
**Previous Interpretation**: {previous_interpretation}

**Follow-up Question**: {follow_up_question}

Provide a response that:
1. Honors the context of the previous reading
2. Builds on that foundation
3. Addresses the new question directly
4. Deepens rather than repeats the interpretation

Keep the voice consistent with the Hermetic and Jungian principles. Remember: you are illuminating their own wisdom."""

    @staticmethod
    def format_card_info(card: dict[str, Any], is_reversed: bool = False) -> str:
        """Format a card for inclusion in a prompt.

        Args:
            card: Card data dictionary
            is_reversed: Whether the card is reversed

        Returns:
            str: Formatted card information
        """
        name = card.get("name", "Unknown")
        reversal_tag = " (Reversed)" if is_reversed else ""
        return f"{name}{reversal_tag}"

    @staticmethod
    def get_three_card_prompt(
        question: str,
        past_card: dict[str, Any],
        present_card: dict[str, Any],
        future_card: dict[str, Any],
        past_reversed: bool = False,
        present_reversed: bool = False,
        future_reversed: bool = False,
    ) -> str:
        """Generate a three-card spread prompt.

        Args:
            question: The querent's question
            past_card: Card data for Past position
            present_card: Card data for Present position
            future_card: Card data for Future position
            past_reversed: Whether past card is reversed
            present_reversed: Whether present card is reversed
            future_reversed: Whether future card is reversed

        Returns:
            str: Formatted prompt for LLM
        """
        return PromptTemplates.THREE_CARD_TEMPLATE.format(
            question=question,
            past_card=PromptTemplates.format_card_info(past_card, past_reversed),
            past_reversal="This card is reversed, suggesting blocked or shadow energy."
            if past_reversed
            else "",
            present_card=PromptTemplates.format_card_info(
                present_card, present_reversed
            ),
            present_reversal="This card is reversed, suggesting blocked or shadow energy."
            if present_reversed
            else "",
            future_card=PromptTemplates.format_card_info(future_card, future_reversed),
            future_reversal="This card is reversed, suggesting blocked or shadow energy."
            if future_reversed
            else "",
        )
