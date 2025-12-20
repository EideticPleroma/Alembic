# Three-Card Reading Prompt

## Overview

The three-card spread is the foundational spread: Past, Present, Future. It provides sufficient depth for meaningful reflection on any life situation.

## Template Structure

The prompt is defined in `backend/app/core/llm/prompts.py` as `THREE_CARD_TEMPLATE`.

### Input Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `question` | User's question | "What should I focus on in my career?" |
| `past_card` | Card name with reversal | "The Fool (Reversed)" |
| `past_reversal` | Reversal note | "- This card is reversed..." |
| `present_card` | Card name with reversal | "The Magician" |
| `present_reversal` | Reversal note | "" |
| `future_card` | Card name with reversal | "Ace of Cups" |
| `future_reversal` | Reversal note | "" |

### Expected Output Structure

```markdown
## The Cards Speak

### Past: [Card Name]
[2-3 sentence interpretation of the Past card]

### Present: [Card Name]
[2-3 sentence interpretation of the Present card]

### Future: [Card Name]
[2-3 sentence interpretation of the Future card]

## The Weaving
[3-4 sentence narrative connecting all three cards]

## Reflection Questions
- [Question about past card]
- [Question about present card]
- [Question about future card]
```

## Position Meanings

| Position | Meaning | Guidance Question |
|----------|---------|-------------------|
| **Past** | The influences and experiences that brought you here | What foundation or cycle are you completing? |
| **Present** | The current energies and circumstances | What is the true nature of your situation right now? |
| **Future** | The potential outcome and energies ahead | What is trying to emerge? What is the next chapter? |

## Example Output

**Question**: "What should I focus on in my career?"

**Cards**: The Fool, The Magician (Reversed), Ace of Cups

> ## The Cards Speak
>
> ### Past: The Fool
> Your career journey began with a leap of faith - perhaps a new role, a bold decision, or a moment when you chose possibility over certainty. This innocent courage has shaped where you stand now, reminding you that beginnings hold their own wisdom.
>
> ### Present: The Magician (Reversed)
> Your creative power and will may be blocked or misdirected right now. The Magician reversed suggests scattered energy - perhaps too many projects, unclear purpose, or imposter syndrome whispering that you lack skills you actually possess. The tools are in your hands, but something prevents their full use.
>
> ### Future: Ace of Cups
> A striking shift emerges - from mental/willful energy to emotional/intuitive flow. This suggests your career focus may benefit from considering not just what you can do, but what fills your cup. New emotional beginnings, creative inspiration, or work that feeds the soul awaits.
>
> ## The Weaving
> Together, these cards weave a narrative of evolution: from innocent beginning, through a current struggle with blocked will, toward a future where heart leads. The Principle of Rhythm reminds us that all things flow - the blockage of the reversed Magician is temporary, a trough before the next crest.
>
> ## Reflection Questions
> - What wisdom from your initial leap of faith still applies today?
> - Where is your energy scattered, and what would focus look like?
> - What work would you do even if no one was watching or paying?
