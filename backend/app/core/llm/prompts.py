"""Prompt templates for tarot interpretation.

Hermetic principles and Jungian psychology guide the interpretation voice.
"""

from typing import Any


class PromptTemplates:
    """Collection of system and user prompts for tarot readings."""

    SYSTEM_PROMPT = """You are Alembic, an AI oracle rooted in Hermetic philosophy and Jungian depth psychology.

Your role is to interpret tarot readings as mirrors for the querent's inner world - not to predict the future, but to illuminate patterns, shadow aspects, and potential pathways.

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

Format your response with clear markdown headers (## and ###) to structure the interpretation. Do NOT include any meta-instructions, format markers, or bracketed placeholders in your response.

Remember: You are a guide to the querent's own wisdom. The cards are the message; you are the messenger."""

    # =========================================================================
    # ONE CARD TEMPLATE
    # =========================================================================
    ONE_CARD_TEMPLATE = """A seeker has drawn a single card for guidance and reflection.

**Question**: {question}

**The Card**: {card_name} {reversal_note}

Provide an interpretation using this structure:

## The Card Speaks
Interpret this single card deeply - its imagery, symbolism, and message for the querent. Consider the card's archetype and how it speaks to their question. (3-4 sentences)

## The Mirror
What does this card reflect about the querent's situation? What pattern or truth is being illuminated? (2-3 sentences)

## Reflection Questions
Offer 2-3 questions for the querent to sit with, drawn from the card's wisdom.

Speak directly to the querent using "you" language. Be wise but warm."""

    # =========================================================================
    # THREE CARD TEMPLATE
    # =========================================================================
    THREE_CARD_TEMPLATE = """A seeker has drawn three cards for reflection on their situation.

**Question**: {question}

**The Reading**:
- **Past** (Foundation): {past_card} {past_reversal}
- **Present** (Current energy): {present_card} {present_reversal}
- **Future** (Emerging potential): {future_card} {future_reversal}

Provide an interpretation using this structure:

## The Cards Speak

### Past: {past_card_name}
Interpret the Past card - what foundation or cycle is completing? How did the querent arrive here? (2-3 sentences)

### Present: {present_card_name}
Interpret the Present card - what is the true nature of their current situation? What energy surrounds them now? (2-3 sentences)

### Future: {future_card_name}
Interpret the Future card - what potential is emerging? What is trying to manifest? (2-3 sentences)

## The Weaving
Connect all three cards into a coherent narrative. How does the story flow from past through present toward future? What is the overall message? (3-4 sentences)

## Reflection Questions
Offer 3 questions for the querent - one related to each card position.

Speak directly to the querent using "you" language. Be wise but warm."""

    # =========================================================================
    # SHADOW WORK TEMPLATE
    # =========================================================================
    SHADOW_WORK_TEMPLATE = """A seeker has drawn four cards for deep shadow work - exploring denied aspects of self.

**Question**: {question}

**The Shadow Reading**:
- **What I Deny** (The rejected aspect): {deny_card} {deny_reversal}
- **Why I Hide It** (The fear beneath): {hide_card} {hide_reversal}
- **Its Gift** (The hidden power): {gift_card} {gift_reversal}
- **Integration Path** (The way forward): {integration_card} {integration_reversal}

This is deep psychological work. Approach with compassion and care.

Provide an interpretation using this structure:

## The Shadow Speaks

### What I Deny: {deny_card_name}
What aspect of self is being rejected or pushed into shadow? What quality does the querent judge in others that they possess themselves? (2-3 sentences)

### Why I Hide It: {hide_card_name}
What fear or belief causes this repression? What does the querent believe will happen if they claim this aspect? (2-3 sentences)

### Its Gift: {gift_card_name}
What positive potential lies within this shadow aspect? How could this repressed energy serve the querent if integrated? (2-3 sentences)

### Integration Path: {integration_card_name}
How can the querent begin to acknowledge and integrate this shadow? What action or practice opens them to wholeness? (2-3 sentences)

## The Alchemy
Weave these four aspects into a coherent understanding. What is the querent's shadow trying to teach them? What wholeness awaits on the other side of this work? (3-4 sentences)

## Reflection Questions
Offer 3-4 questions for deep contemplation, guiding the querent toward integration.

This is sacred work. Speak with compassion, honoring both the difficulty and the gift of shadow integration."""

    # =========================================================================
    # CELTIC CROSS TEMPLATE
    # =========================================================================
    CELTIC_CROSS_TEMPLATE = """A seeker has drawn ten cards in the Celtic Cross - a comprehensive exploration of their situation.

**Question**: {question}

**The Celtic Cross**:
1. **Significator** (Heart of the matter): {card_0} {reversal_0}
2. **Challenge** (What crosses you): {card_1} {reversal_1}
3. **Root** (Foundation/Origin): {card_2} {reversal_2}
4. **Recent Past** (What's passing): {card_3} {reversal_3}
5. **Possible Outcome** (Crown/Best outcome): {card_4} {reversal_4}
6. **Near Future** (What's approaching): {card_5} {reversal_5}
7. **Your Attitude** (Your position): {card_6} {reversal_6}
8. **Others' Influence** (External forces): {card_7} {reversal_7}
9. **Hopes and Fears** (Inner landscape): {card_8} {reversal_8}
10. **Outcome** (Final resolution): {card_9} {reversal_9}

Provide an interpretation using this structure:

## The Cross (Central Situation)

### The Heart: {card_0_name}
What is this situation truly about at its core? (2 sentences)

### The Challenge: {card_1_name}
What obstacle or influence must be navigated? (2 sentences)

### The Root: {card_2_name}
Where does this situation originate? What foundation supports it? (2 sentences)

### Recent Past: {card_3_name}
What influence is now passing away? (2 sentences)

### Crown: {card_4_name}
What is the highest potential outcome? (2 sentences)

### Near Future: {card_5_name}
What energy is approaching? (2 sentences)

## The Staff (Surrounding Influences)

### Your Position: {card_6_name}
How is the querent approaching this situation? (2 sentences)

### External Forces: {card_7_name}
What are others or external circumstances contributing? (2 sentences)

### Hopes and Fears: {card_8_name}
What does the querent deeply desire or fear? (2 sentences)

### Ultimate Outcome: {card_9_name}
What is the trajectory and lesson here? (2 sentences)

## The Synthesis
Weave the entire spread into a coherent narrative. What is the full picture? What guidance emerges from seeing all cards together? (4-5 sentences)

## Reflection Questions
Offer 3-4 questions that help the querent integrate this comprehensive reading.

Speak directly to the querent with wisdom and warmth."""

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

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

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
    def get_reversal_note(is_reversed: bool) -> str:
        """Get the reversal note for a card.

        Args:
            is_reversed: Whether the card is reversed

        Returns:
            str: Reversal note or empty string
        """
        if is_reversed:
            return "- This card is reversed, suggesting blocked or shadow energy."
        return ""

    @staticmethod
    def get_one_card_prompt(
        question: str,
        card: dict[str, Any],
        is_reversed: bool = False,
    ) -> str:
        """Generate a one-card spread prompt.

        Args:
            question: The querent's question
            card: Card data
            is_reversed: Whether the card is reversed

        Returns:
            str: Formatted prompt for LLM
        """
        return PromptTemplates.ONE_CARD_TEMPLATE.format(
            question=question,
            card_name=PromptTemplates.format_card_info(card, is_reversed),
            reversal_note=PromptTemplates.get_reversal_note(is_reversed),
        )

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
            past_reversal=PromptTemplates.get_reversal_note(past_reversed),
            past_card_name=past_card.get("name", "Unknown"),
            present_card=PromptTemplates.format_card_info(
                present_card, present_reversed
            ),
            present_reversal=PromptTemplates.get_reversal_note(present_reversed),
            present_card_name=present_card.get("name", "Unknown"),
            future_card=PromptTemplates.format_card_info(future_card, future_reversed),
            future_reversal=PromptTemplates.get_reversal_note(future_reversed),
            future_card_name=future_card.get("name", "Unknown"),
        )

    @staticmethod
    def get_shadow_work_prompt(
        question: str,
        cards: list[dict[str, Any]],
    ) -> str:
        """Generate a shadow work spread prompt.

        Args:
            question: The querent's question
            cards: List of 4 cards with is_reversed field

        Returns:
            str: Formatted prompt for LLM
        """
        deny_card = cards[0]
        hide_card = cards[1]
        gift_card = cards[2]
        integration_card = cards[3]

        return PromptTemplates.SHADOW_WORK_TEMPLATE.format(
            question=question,
            deny_card=PromptTemplates.format_card_info(
                deny_card, deny_card.get("is_reversed", False)
            ),
            deny_reversal=PromptTemplates.get_reversal_note(
                deny_card.get("is_reversed", False)
            ),
            deny_card_name=deny_card.get("name", "Unknown"),
            hide_card=PromptTemplates.format_card_info(
                hide_card, hide_card.get("is_reversed", False)
            ),
            hide_reversal=PromptTemplates.get_reversal_note(
                hide_card.get("is_reversed", False)
            ),
            hide_card_name=hide_card.get("name", "Unknown"),
            gift_card=PromptTemplates.format_card_info(
                gift_card, gift_card.get("is_reversed", False)
            ),
            gift_reversal=PromptTemplates.get_reversal_note(
                gift_card.get("is_reversed", False)
            ),
            gift_card_name=gift_card.get("name", "Unknown"),
            integration_card=PromptTemplates.format_card_info(
                integration_card, integration_card.get("is_reversed", False)
            ),
            integration_reversal=PromptTemplates.get_reversal_note(
                integration_card.get("is_reversed", False)
            ),
            integration_card_name=integration_card.get("name", "Unknown"),
        )

    @staticmethod
    def get_celtic_cross_prompt(
        question: str,
        cards: list[dict[str, Any]],
    ) -> str:
        """Generate a Celtic Cross spread prompt.

        Args:
            question: The querent's question
            cards: List of 10 cards with is_reversed field

        Returns:
            str: Formatted prompt for LLM
        """
        format_args: dict[str, str] = {"question": question}

        for i, card in enumerate(cards):
            is_reversed = card.get("is_reversed", False)
            format_args[f"card_{i}"] = PromptTemplates.format_card_info(
                card, is_reversed
            )
            format_args[f"reversal_{i}"] = PromptTemplates.get_reversal_note(
                is_reversed
            )
            format_args[f"card_{i}_name"] = card.get("name", "Unknown")

        return PromptTemplates.CELTIC_CROSS_TEMPLATE.format(**format_args)
