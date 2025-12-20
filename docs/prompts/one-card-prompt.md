# One-Card Reading Prompt

## Overview

The one-card spread is a single powerful card for daily guidance or specific focus. Simple but profound.

## Template Structure

The prompt is defined in `backend/app/core/llm/prompts.py` as `ONE_CARD_TEMPLATE`.

### Input Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `question` | User's question | "What do I need to know today?" |
| `card_name` | Card name with reversal | "The Star (Reversed)" |
| `reversal_note` | Reversal note | "- This card is reversed..." |

### Expected Output Structure

```markdown
## The Card Speaks
[3-4 sentence deep interpretation of the card's imagery, symbolism, and message]

## The Mirror
[2-3 sentences about what this card reflects about the querent's situation]

## Reflection Questions
- [Question 1]
- [Question 2]
- [Question 3]
```

## Position Meaning

| Position | Meaning | Guidance Question |
|----------|---------|-------------------|
| **Message** | The card's message for you today | What is this card showing you? |

## Example Output

**Question**: "What do I need to know today?"

**Card**: The Star

> ## The Card Speaks
> The Star emerges from the darkness that follows The Tower - she is hope after upheaval, healing after crisis. Her waters flow freely, one stream to the earth (material world), one to the pool (emotional/spiritual realm), suggesting the importance of nourishing both aspects of your life. The eight-pointed stars above remind you of the Hermetic principle "As above, so below" - what you tend within reflects in your outer circumstances.
>
> ## The Mirror
> This card suggests you are in a period of renewal, whether you recognize it or not. After whatever storms have passed, there is an invitation to trust again, to pour yourself into life without holding back. Your hope is not naive - it is earned.
>
> ## Reflection Questions
> - What is being renewed in your life right now?
> - Where might you be holding back from fully trusting the flow?
> - How can you nourish both your practical and spiritual needs today?
