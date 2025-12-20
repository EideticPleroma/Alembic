# Celtic Cross Spread Prompt

## Overview

The Celtic Cross is a comprehensive 10-card spread exploring all dimensions of a situation. This classic spread provides nuanced insight including hidden influences and potential outcomes.

## Template Structure

The prompt is defined in `backend/app/core/llm/prompts.py` as `CELTIC_CROSS_TEMPLATE`.

### Input Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `question` | User's question | "Should I change careers?" |
| `card_0` - `card_9` | Card names with reversal | "The Fool (Reversed)" |
| `reversal_0` - `reversal_9` | Reversal notes | "- This card is reversed..." |

### Expected Output Structure

```markdown
## The Cross (Central Situation)

### The Heart: [Card 0]
[2 sentences about what this situation is truly about]

### The Challenge: [Card 1]
[2 sentences about the obstacle to navigate]

### The Root: [Card 2]
[2 sentences about the origin/foundation]

### Recent Past: [Card 3]
[2 sentences about what's passing]

### Crown: [Card 4]
[2 sentences about highest potential]

### Near Future: [Card 5]
[2 sentences about approaching energy]

## The Staff (Surrounding Influences)

### Your Position: [Card 6]
[2 sentences about querent's approach]

### External Forces: [Card 7]
[2 sentences about others' influence]

### Hopes and Fears: [Card 8]
[2 sentences about inner landscape]

### Ultimate Outcome: [Card 9]
[2 sentences about trajectory and lesson]

## The Synthesis
[4-5 sentences weaving the full picture together]

## Reflection Questions
- [Question 1]
- [Question 2]
- [Question 3]
- [Question 4]
```

## Position Meanings

| # | Position | Meaning | Guidance Question |
|---|----------|---------|-------------------|
| 1 | **Significator** | The heart of the matter | What is this really about? |
| 2 | **Challenge** | The obstacle or influence to navigate | What is the true challenge? |
| 3 | **Root** | The foundation or origin | Where does this come from? |
| 4 | **Recent Past** | Recent influences that shaped present | What just happened? |
| 5 | **Possible Outcome** | Where things are naturally heading | What is the likely path? |
| 6 | **Near Future** | Energies coming into play soon | What is emerging? |
| 7 | **Your Attitude** | Your role and perspective | How are you approaching this? |
| 8 | **Others' Influence** | External forces and people | What are others bringing? |
| 9 | **Hopes/Fears** | Deeper desires or anxieties | What do you really want? What scares you? |
| 10 | **Outcome** | The ultimate resolution or lesson | What is being revealed? |

## Layout Diagram

```
        [5]
         |
    [4]-[1/2]-[6]
         |
        [3]

    [7]
    [8]
    [9]
    [10]
```

The Cross (positions 1-6) represents the situation itself.
The Staff (positions 7-10) represents surrounding influences and trajectory.

## Interpretation Approach

Given the complexity of this spread:

1. **Start with the Heart** (pos 1) - ground the reading
2. **Identify the Challenge** (pos 2) - name the tension
3. **Trace the Timeline** (pos 3-6) - past through future
4. **Examine External Factors** (pos 7-8) - self and others
5. **Acknowledge Inner World** (pos 9) - hopes and fears
6. **Synthesize to Outcome** (pos 10) - the learning

The synthesis section is crucial for this spread - with 10 cards, the querent needs help seeing the coherent story.
