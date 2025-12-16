# Tarot Spreads

## Overview

Alembic supports multiple spread types, starting with the three-card spread for MVP.

## Three-Card Spread (MVP)

The foundational spread for understanding situations across time.

### Layout

```
  [1]        [2]        [3]
  Past     Present    Future
```

### Positions

| Position | Name | Meaning |
|----------|------|---------|
| 1 | Past | What has been - influences, patterns, or energies that have shaped the current situation |
| 2 | Present | What is - the current state, active energies, or the crossroads where you stand |
| 3 | Future | What emerges - the trajectory, potential outcome, or emerging energy (not prediction) |

### Interpretive Focus

- **Narrative arc**: How does the story flow from past through present to future?
- **Principle of Rhythm**: What cycle or pattern is visible?
- **Evolution**: Is there growth, stagnation, or regression?

### Implementation

```python
class ThreeCardSpread:
    name = "Three Card"
    card_count = 3
    positions = ["Past", "Present", "Future"]
    description = "Understanding a situation through time"
    credit_cost = 1
    
    @staticmethod
    def get_prompt_context() -> str:
        return """
        The Past position reveals what has shaped the situation.
        The Present position shows the current dynamic or crossroads.
        The Future position suggests what energy is emerging (not predicting).
        """
```

---

## Single Card (Daily Guidance)

A simple draw for daily reflection or quick insight.

### Layout

```
  [1]
 Focus
```

### Positions

| Position | Name | Meaning |
|----------|------|---------|
| 1 | Focus | The energy, archetype, or message most relevant today |

### Interpretive Focus

- **Daily theme**: What archetype wants your attention?
- **Meditation seed**: A symbol to carry through the day
- **Principle of Mentalism**: What mindset does this card invite?

### Implementation

```python
class SingleCardSpread:
    name = "Single Card"
    card_count = 1
    positions = ["Focus"]
    description = "Daily guidance or quick insight"
    credit_cost = 1
```

---

## Shadow Work Spread (Phase 2)

A Jungian-focused spread for exploring the shadow.

### Layout

```
     [1]
   Persona
  
[2]      [3]
Shadow   Integration
```

### Positions

| Position | Name | Meaning |
|----------|------|---------|
| 1 | Persona | How you present to the world; the mask |
| 2 | Shadow | What you hide, deny, or project onto others |
| 3 | Integration | The path to wholeness; how to reconcile |

### Interpretive Focus

- **Jungian framework**: Persona vs Shadow
- **Principle of Polarity**: Opposites are identical in nature
- **Individuation**: The journey toward wholeness

### Implementation

```python
class ShadowWorkSpread:
    name = "Shadow Work"
    card_count = 3
    positions = ["Persona", "Shadow", "Integration"]
    description = "Exploring the unconscious through Jungian archetypes"
    credit_cost = 2
```

---

## Celtic Cross (Phase 3)

The comprehensive traditional spread for deep life analysis.

### Layout

```
                [5]
                Crown
                
    [4]         [1]         [6]
  Recent       Signif.      Near
   Past        [2]Cross     Future
                
                [3]
              Foundation
              
[10] Outcome
[9]  Hopes/Fears
[8]  Environment
[7]  Self
```

### Positions

| Position | Name | Meaning |
|----------|------|---------|
| 1 | Significator | The heart of the matter; current situation |
| 2 | Crossing | The challenge or opposition |
| 3 | Foundation | Root cause; unconscious influences |
| 4 | Recent Past | What is passing or has just occurred |
| 5 | Crown | Best possible outcome; conscious goal |
| 6 | Near Future | What approaches in the short term |
| 7 | Self | Your inner state; how you see yourself |
| 8 | Environment | External influences; how others see you |
| 9 | Hopes/Fears | Inner hopes or fears (often the same) |
| 10 | Outcome | The resolution; where things are heading |

### Interpretive Focus

- **Full life analysis**: Multiple dimensions of a situation
- **Principle of Correspondence**: Internal and external mirrors
- **Synthesis**: Weaving 10 cards into coherent narrative

### Implementation

```python
class CelticCrossSpread:
    name = "Celtic Cross"
    card_count = 10
    positions = [
        "Significator", "Crossing", "Foundation", "Recent Past",
        "Crown", "Near Future", "Self", "Environment",
        "Hopes/Fears", "Outcome"
    ]
    description = "Comprehensive analysis for complex situations"
    credit_cost = 3
```

---

## Spread Configuration

### Database Schema

```sql
-- Spreads can be stored for extensibility
CREATE TABLE spread_types (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    card_count INTEGER NOT NULL,
    positions JSONB NOT NULL,
    credit_cost INTEGER NOT NULL DEFAULT 1,
    is_premium BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed data
INSERT INTO spread_types (id, name, card_count, positions, credit_cost, is_premium)
VALUES 
    ('single', 'Single Card', 1, '["Focus"]', 1, false),
    ('three_card', 'Three Card', 3, '["Past", "Present", "Future"]', 1, false),
    ('shadow_work', 'Shadow Work', 3, '["Persona", "Shadow", "Integration"]', 2, true),
    ('celtic_cross', 'Celtic Cross', 10, '["Significator", "Crossing", "Foundation", "Recent Past", "Crown", "Near Future", "Self", "Environment", "Hopes/Fears", "Outcome"]', 3, true);
```

### Adding New Spreads

1. Define the spread class with positions and meanings
2. Add to database or configuration
3. Create specific prompt template in `docs/prompts/`
4. Update pricing if needed
5. Add to UI spread selector

