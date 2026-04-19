import json
import os
from typing import Optional
from game.colours import Colours, colourize

BOSS_SAVE_FILE = "json_files/previous_boss.json"


def save_character_as_boss(character_data: dict) -> None:
    """
    Save the current character's data to be used as the final boss in future playthroughs.

    The boss will have:
    - The character's name (as the boss name)
    - Scaled-up stats based on their level
    - A selection of their class actions converted to enemy attacks
    """
    character = character_data["character"]


    base_hp = character["base_stats"]["constitution"] * character["derived_stats"]["max_health"]["multiplier"]
    level = character["level"]


    boss_health = int(base_hp * (1 + (level - 1) * 0.5) + 50)


    attacks = []

    # Get class actions from character's level
    # Note: You'll need to pass class_data or load it here
    # For now, we'll create generic attacks based on stats

    attacks = [
        {
            "name": "Heroic Strike",
            "damage": int(character["base_stats"]["strength"] * (1 + level * 0.3)),
            "description": f"{character['name']} strikes with incredible force!"
        },
        {
            "name": "Arcane Burst",
            "damage": int(character["base_stats"]["intellect"] * (1 + level * 0.3)),
            "description": f"{character['name']} unleashes a burst of magical energy!"
        },
        {
            "name": "Relentless Assault",
            "damage": int(
                (character["base_stats"]["strength"] + character["base_stats"]["dexterity"]) * (0.8 + level * 0.2)),
            "description": f"{character['name']} attacks with relentless fury!"
        },
        {
            "name": "Final Stand",
            "damage": int(character["base_stats"]["constitution"] * (1.5 + level * 0.2)),
            "description": f"{character['name']} gathers their remaining strength for a devastating blow!"
        }
    ]

    boss_data = {
        "id": 12,
        "type": "boss",
        "name": f"Shadow of {character['name']}",
        "description": f"A dark reflection of {character['name']} stands before you, corrupted by the dungeon's power.",
        "enemy": {
            "name": f"Shadow of {character['name']}",
            "health": boss_health,
            "attacks": attacks,
            "original_player_name": character["name"],
            "original_class": character["class"],
            "original_level": level
        },
        "defeated_by": None
    }


    with open(BOSS_SAVE_FILE, 'w') as f:
        json.dump(boss_data, f, indent=2)

    print(colourize(f"\n✨ Your character's shadow has been etched into the dungeon! ✨", Colours.SPECIAL))
    print(colourize(f"Future heroes will face the corrupted memory of {character['name']}...", Colours.WARNING))


def load_previous_boss() -> Optional[dict]:
    """
    Load the previously saved boss character data.
    Returns None if no boss data exists.
    """
    if os.path.exists(BOSS_SAVE_FILE):
        with open(BOSS_SAVE_FILE, 'r') as f:
            return json.load(f)
    return None


def has_previous_boss() -> bool:
    """Check if a previous boss save exists."""
    return os.path.exists(BOSS_SAVE_FILE)