# Shadow Work Spread Prompt

## Overview

The Shadow Work spread is a 4-card spread for integrating shadow aspects and unconscious patterns. This is deep psychological work based on Jungian principles.

## Template Structure

The prompt is defined in `backend/app/core/llm/prompts.py` as `SHADOW_WORK_TEMPLATE`.

### Input Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `question` | User's question | "What shadow am I avoiding?" |
| `deny_card` | Card name with reversal | "The Emperor (Reversed)" |
| `deny_reversal` | Reversal note | "- This card is reversed..." |
| `hide_card` | Card name with reversal | "Nine of Swords" |
| `hide_reversal` | Reversal note | "" |
| `gift_card` | Card name with reversal | "Strength" |
| `gift_reversal` | Reversal note | "" |
| `integration_card` | Card name with reversal | "The Hermit" |
| `integration_reversal` | Reversal note | "" |

### Expected Output Structure

```markdown
## The Shadow Speaks

### What I Deny: [Card Name]
[2-3 sentences about the rejected aspect of self]

### Why I Hide It: [Card Name]
[2-3 sentences about the fear or belief causing repression]

### Its Gift: [Card Name]
[2-3 sentences about the positive potential of this shadow aspect]

### Integration Path: [Card Name]
[2-3 sentences about how to integrate this shadow]

## The Alchemy
[3-4 sentences weaving all four aspects into a coherent understanding]

## Reflection Questions
- [Question 1]
- [Question 2]
- [Question 3]
- [Question 4]
```

## Position Meanings

| Position | Meaning | Guidance Question |
|----------|---------|-------------------|
| **What I Deny** | The aspect of myself I reject or don't acknowledge | What quality do I judge in others that I possess? |
| **Why I Hide It** | The fear or belief that causes repression | What am I afraid will happen if I claim this? |
| **Its Gift** | The positive potential of this shadow aspect | How could this power serve me if integrated? |
| **Integration Path** | How to bring this aspect into consciousness | What action opens me to wholeness? |

## Therapeutic Approach

This spread requires extra compassion in interpretation:

1. **Normalize** - Shadow work is universal human experience
2. **Honor the defense** - Repression served a protective purpose
3. **Illuminate the gift** - Every shadow contains gold
4. **Offer gentle path** - Integration is a process, not an event

## Example Output

**Question**: "What shadow am I avoiding in my relationships?"

**Cards**: The Emperor (Reversed), Nine of Swords, Strength, The Hermit

> ## The Shadow Speaks
>
> ### What I Deny: The Emperor (Reversed)
> You may be rejecting your own authority and power - perhaps the capacity to set boundaries, make decisions, or take up space. The reversed Emperor suggests an ambivalent relationship with control; you may judge others as "controlling" while denying your own need to direct your life.
>
> ### Why I Hide It: Nine of Swords
> The fear runs deep - perhaps anxiety about being seen as demanding, bossy, or unlovable if you claim your power. The Nine of Swords speaks to catastrophic thinking, midnight worries that if you truly stood in your authority, others would leave or attack. These fears likely have roots in earlier experiences.
>
> ### Its Gift: Strength
> But here is the gold in your shadow! True Strength is not domination but sovereign presence - the lion tamed not by force but by love. Your repressed authority, when integrated, becomes the capacity to be powerful AND compassionate, to lead without controlling, to hold boundaries while remaining soft.
>
> ### Integration Path: The Hermit
> The path forward involves turning inward - time alone with yourself, perhaps journaling or meditation, to meet this shadow aspect with curiosity rather than judgment. The Hermit's lantern illuminates what has been hidden. Small acts of claiming your space, speaking your needs, making decisions without excessive consultation.
>
> ## The Alchemy
> Your shadow work reveals a pattern: early experiences taught you that power was dangerous, leading to anxiety about authority. Yet the very power you reject is trying to mature into Strength - sovereign, compassionate presence. The Hermit suggests this integration happens gradually, through inner work and small brave acts of self-assertion.
>
> ## Reflection Questions
> - When you judge someone as "controlling," what quality in yourself does this mirror?
> - What did you learn early about what happens to people who take up space?
> - How might healthy authority actually serve your relationships?
> - What small act of claiming your power could you practice this week?
