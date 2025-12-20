#!/usr/bin/env python3
"""Add missing metadata fields to minor arcana cards."""

import json
from pathlib import Path

# Load the cards data
cards_file = Path("backend/app/core/tarot/data/cards.json")
with open(cards_file, "r") as f:
    data = json.load(f)

# Mapping of suits to their hermetic principles and general archetypes
suit_info = {
    "wands": {
        "hermetic_principle": "Correspondence",
        "archetype": "The Creator",
        "keywords_base": ["fire", "creation", "passion", "action"],
    },
    "cups": {
        "hermetic_principle": "Polarity",
        "archetype": "The Lover",
        "keywords_base": ["water", "emotion", "intuition", "connection"],
    },
    "swords": {
        "hermetic_principle": "Rhythm",
        "archetype": "The Thinker",
        "keywords_base": ["air", "intellect", "truth", "clarity"],
    },
    "pentacles": {
        "hermetic_principle": "Mentalism",
        "archetype": "The Keeper",
        "keywords_base": ["earth", "material", "manifestation", "abundance"],
    },
}

# Add missing fields to minor arcana
for suit_name, suit_data in data["minor_arcana"].items():
    if "cards" in suit_data:
        suit_base = suit_info.get(suit_name, {})
        for card in suit_data["cards"]:
            # Add keywords if missing
            if "keywords" not in card:
                card["keywords"] = list(suit_base.get("keywords_base", []))

            # Add archetype if missing
            if "archetype" not in card:
                card["archetype"] = suit_base.get("archetype", "The Card")

            # Add hermetic principle if missing
            if "hermetic_principle" not in card:
                card["hermetic_principle"] = suit_base.get(
                    "hermetic_principle", "Correspondence"
                )

# Write back
with open(cards_file, "w") as f:
    json.dump(data, f, indent=2)

print("[OK] Added missing fields to minor arcana cards")
