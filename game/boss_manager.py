import json
import os
import random
from typing import Optional
from game.colours import Colours, colourize

BOSS_SAVE_FILE = "json_files/previous_boss.json"


def save_character_as_boss(character_data: dict, class_data: dict = None) -> None:
    """
    Save the current character's data to be used as the final boss in future playthroughs.

    The boss will have:
    - The character's name (as the boss name)
    - Scaled-up stats based on their level
    - Their actual class actions converted to enemy attacks
    """
    character = character_data["character"]

    # Calculate scaled boss stats
    base_hp = character["base_stats"]["constitution"] * character["derived_stats"]["max_health"]["multiplier"]
    level = character["level"]

    # Scale health based on level (boss gets extra health)
    boss_health = int(base_hp * (1 + (level - 1) * 0.5) + 100)

    # Get character's actions from their class
    attacks = convert_actions_to_boss_attacks(character, class_data)

    # If no actions were converted, create fallback attacks based on stats
    if not attacks:
        attacks = create_fallback_attacks(character)

    boss_data = {
        "id": 12,  # Boss ID
        "type": "boss",
        "name": f"Shadow of {character['name']}",
        "description": f"A dark reflection of {character['name']} stands before you, corrupted by the dungeon's power.",
        "enemy": {
            "name": f"Shadow of {character['name']}",
            "health": boss_health,
            "attacks": attacks,
            "original_player_name": character["name"],
            "original_class": character["class"],
            "original_level": level,
            "original_stats": dict(character["base_stats"])
        },
        "defeated_by": None  # Will track who defeated this boss
    }

    # Save to file
    with open(BOSS_SAVE_FILE, 'w') as f:
        json.dump(boss_data, f, indent=2)

    print(colourize(f"\n✨ Your character's shadow has been etched into the dungeon! ✨", Colours.SPECIAL))
    print(colourize(f"   Level {level} {character['class']} - {character['name']}", Colours.TITLE))
    print(colourize(f"   Future heroes will face your corrupted memory...", Colours.WARNING))


def convert_actions_to_boss_attacks(character: dict, class_data: dict) -> list:
    """
    Convert character's class actions into boss attacks.
    """
    attacks = []

    if not class_data:
        return attacks

    character_class = character["class"]
    level = str(character["level"])

    # Find the character's pathway
    pathway = None
    for pathway_data in class_data.values():
        if pathway_data["name"] == character_class:
            pathway = pathway_data
            break

    if not pathway:
        return attacks

    # Get actions for the character's level
    level_data = pathway["level"].get(level)
    if not level_data:
        # Try to get highest available level
        available_levels = [int(lvl) for lvl in pathway["level"].keys()]
        if available_levels:
            highest = str(max(available_levels))
            level_data = pathway["level"][highest]

    if not level_data:
        return attacks

    actions = level_data.get("actions", {})

    # Convert up to 4 actions to boss attacks
    action_keys = list(actions.keys())
    selected_actions = random.sample(action_keys, min(4, len(action_keys)))

    for action_key in selected_actions:
        action = actions[action_key]
        boss_attack = convert_action_to_boss_attack(action, character, action_key)
        attacks.append(boss_attack)

    # Ensure we have at least 3 attacks
    while len(attacks) < 3:
        attacks.append(create_fallback_attack(character, len(attacks)))

    return attacks


def convert_action_to_boss_attack(action: dict, character: dict, action_key: str) -> dict:
    """
    Convert a player action into a boss attack.
    """
    from game.combat import calculate_damage

    action_name = action.get("name", action_key.capitalize())
    action_type = action.get("type", "attack")

    # Calculate base damage based on character's stats
    if action_type == "attack":
        # Calculate damage using the action's scaling
        scaling = action.get("scaling", {})
        if scaling:
            if isinstance(scaling, list):
                damage = 0
                for scale in scaling:
                    stat_value = character["base_stats"].get(scale.get("stat", "strength"), 10)
                    damage += stat_value * scale.get("multiplier", 1)
            else:
                stat_value = character["base_stats"].get(scaling.get("stat", "strength"), 10)
                damage = stat_value * scaling.get("multiplier", 1)
        else:
            damage = character["base_stats"]["strength"] * 2

        # Scale damage for boss (1.5x to 2x)
        damage = int(damage * random.uniform(1.5, 2.0))

    elif action_type == "heal":
        # Boss heals instead of damages
        damage = int(action.get("amount", 20) * 0.5)  # Half healing as damage
        action_name = f"Corrupted {action_name}"

    elif action_type == "buff":
        # Boss buffs become damaging attacks
        effect = action.get("effect", {})
        amount = effect.get("amount", 2)
        damage = int(amount * 8)
        action_name = f"Corrupted {action_name}"

    else:
        # Default damage calculation
        damage = int(character["base_stats"]["strength"] * 3)

    # Create description
    descriptions = [
        f"The shadow of {character['name']} uses {action_name}!",
        f"Dark energy surges as the shadow performs {action_name}!",
        f"Your own technique turned against you - {action_name}!",
        f"The corrupted memory strikes with {action_name}!"
    ]

    return {
        "name": f"Shadow {action_name}",
        "damage": max(15, damage),  # Minimum 15 damage
        "description": random.choice(descriptions)
    }


def create_fallback_attacks(character: dict) -> list:
    """
    Create fallback attacks based on character's stats.
    """
    attacks = []
    stats = character["base_stats"]

    # Attack based on strength
    attacks.append({
        "name": "Shadow Strike",
        "damage": max(15, int(stats.get("strength", 10) * 3)),
        "description": "The shadow lunges forward with incredible speed!"
    })

    # Attack based on intellect
    attacks.append({
        "name": "Dark Magic",
        "damage": max(15, int(stats.get("intellect", 10) * 3)),
        "description": "A wave of dark energy erupts from the shadow!"
    })

    # Attack based on dexterity
    attacks.append({
        "name": "Shadow Dance",
        "damage": max(15, int(stats.get("dexterity", 10) * 2.5)),
        "description": "The shadow moves like a blur, striking multiple times!"
    })

    # Heavy attack
    attacks.append({
        "name": "Desperation",
        "damage": max(20, int((stats.get("strength", 10) + stats.get("constitution", 10)) * 2)),
        "description": "The shadow gathers all its power for a devastating blow!"
    })

    return attacks


def create_fallback_attack(character: dict, index: int) -> dict:
    """
    Create a single fallback attack.
    """
    attack_templates = [
        ("Shadow Strike", "strength", 3, "The shadow strikes with dark energy!"),
        ("Dark Bolt", "intellect", 3, "A bolt of shadow magic flies toward you!"),
        ("Soul Drain", "intellect", 2.5, "You feel your life force being drained!"),
        ("Shadow Claw", "dexterity", 2.5, "Shadowy claws rake across your body!"),
        ("Dark Pulse", "strength", 2, "A pulse of darkness explodes outward!"),
    ]

    name, stat, multiplier, desc = attack_templates[index % len(attack_templates)]
    damage = int(character["base_stats"].get(stat, 10) * multiplier)

    return {
        "name": name,
        "damage": max(15, damage),
        "description": desc
    }


def load_previous_boss() -> Optional[dict]:
    """
    Load the previously saved boss character data.
    Returns None if no boss data exists.
    """
    if os.path.exists(BOSS_SAVE_FILE):
        try:
            with open(BOSS_SAVE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def has_previous_boss() -> bool:
    """Check if a previous boss save exists."""
    return os.path.exists(BOSS_SAVE_FILE)


def clear_boss_data() -> None:
    """Clear saved boss data (useful for testing)."""
    if os.path.exists(BOSS_SAVE_FILE):
        os.remove(BOSS_SAVE_FILE)