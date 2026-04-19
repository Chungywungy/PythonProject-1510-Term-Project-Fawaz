import random
from game.colours import Colours, colourize, hp_bar, mana_bar
from game.character import equip_item


# In events.py, update handle_chest to properly add equipment items:

def handle_chest(character: dict, event: dict, items_data: dict) -> dict:
    """Handle chest events - can contain items, gold, or traps."""
    chest_name = event["name"]
    chest_type = "common" if "Wooden" in chest_name else "rare" if "Iron" in chest_name else "common"

    print(colourize(f"\n📦 {chest_name}", Colours.SPECIAL))
    print(f"{event['description']}")

    # Random chance for trap (20% for wooden, 40% for iron)
    trap_chance = 0.2 if chest_type == "common" else 0.4

    if random.random() < trap_chance:
        # Trap!
        damage = random.randint(5, 15) if chest_type == "common" else random.randint(10, 25)
        character["character"]["current"]["health"] -= damage
        print(colourize(f"\n💀 A trap activates! You take {damage} damage!", Colours.FAIL))

        # Get max health for display
        constitution = character["character"]["base_stats"]["constitution"]
        max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]
        print(f"❤️ HP: {character['character']['current']['health']}/{max_health}")

        if character["character"]["current"]["health"] <= 0:
            print(colourize("\nThe trap was fatal...", Colours.FAIL))
        return character

    # Determine reward
    if chest_type == "common":
        reward_type = random.choice(["consumable", "equipment", "gold"])

        if reward_type == "consumable":
            # Give a health potion or similar
            consumables = [item for item in items_data["items"] if item["type"] == "consumable"]
            if consumables:
                reward = random.choice(consumables)
                character["character"]["inventory"].append({
                    "name": reward["name"],
                    "type": "consumable",
                    "effect": reward.get("effect", {})
                })
                print(colourize(f"\n✨ You found: {reward['name']}!", Colours.HEAL))

        elif reward_type == "equipment":
            # Give common equipment
            equipment = [item for item in items_data["items"] if item["type"] == "equipment"
                         and "Steel" not in item["name"] and "Iron" not in item["name"]
                         and "Great" not in item["name"] and "Tower" not in item["name"]]
            if equipment:
                reward = random.choice(equipment)
                character["character"]["inventory"].append({
                    "name": reward["name"],
                    "type": "equipment",
                    "slot": reward["slot"],
                    "stats": reward.get("stats", {})
                })
                print(colourize(f"\n✨ You found: {reward['name']}!", Colours.SPECIAL))
                print(f"   Slot: {reward['slot']} | Stats: {reward.get('stats', {})}")

        else:  # gold/xp
            xp_gain = random.randint(10, 25)
            character["character"]["xp"] = character["character"].get("xp", 0) + xp_gain
            print(colourize(f"\n✨ You gained {xp_gain} XP from the chest!", Colours.XP))

    else:  # rare chest (Locked Iron Chest)
        # May require strength check to open
        strength = character["character"]["base_stats"]["strength"]
        difficulty = 12

        print(colourize("\n🔒 The chest is locked!", Colours.WARNING))
        choice = input("Try to force it open? (y/n): ").strip().lower()

        if choice == 'y':
            if strength >= difficulty or random.random() < 0.4:
                print(colourize("\n💪 You force the chest open!", Colours.BUFF))

                # Better rewards
                reward_type = random.choice(["rare_equipment", "consumable", "xp_boost"])

                if reward_type == "rare_equipment":
                    rare_items = [item for item in items_data["items"] if item["type"] == "equipment"
                                  and ("Steel" in item["name"] or "Great" in item["name"] or "Tower" in item["name"]
                                       or "Heavy" in item["name"] or "Elixir" in item["name"])]
                    if rare_items:
                        reward = random.choice(rare_items)
                        character["character"]["inventory"].append({
                            "name": reward["name"],
                            "type": "equipment",
                            "slot": reward["slot"],
                            "stats": reward.get("stats", {})
                        })
                        print(colourize(f"\n🌟 You found rare item: {reward['name']}!", Colours.TITLE))
                        print(f"   Slot: {reward['slot']} | Stats: {reward.get('stats', {})}")

                elif reward_type == "consumable":
                    # Give a rare consumable
                    rare_consumables = ["Experience Scroll", "Ancient Tome", "Elixir of Power", "Rage Potion"]
                    available = [item for item in items_data["items"] if item["name"] in rare_consumables]
                    if available:
                        reward = random.choice(available)
                        character["character"]["inventory"].append({
                            "name": reward["name"],
                            "type": "consumable",
                            "effect": reward.get("effect", {})
                        })
                        print(colourize(f"\n🌟 You found: {reward['name']}!", Colours.TITLE))

                else:  # xp_boost
                    xp_gain = random.randint(30, 60)
                    character["character"]["xp"] = character["character"].get("xp", 0) + xp_gain
                    print(colourize(f"\n🌟 You gained {xp_gain} XP from the chest!", Colours.XP))
            else:
                print(colourize("\n❌ You fail to open the chest. It remains locked.", Colours.FAIL))
        else:
            print(colourize("\nYou leave the chest alone.", Colours.WARNING))

    return character


# Update the handle_boon function in events.py:

def handle_boon(character: dict, event: dict, class_data: dict, items_data: dict) -> dict:
    """Handle boon events - positive blessings that enhance the character."""
    from game.character import get_effective_stats

    boon_name = event["name"]
    description = event["description"]

    print(colourize(f"\n✨ {boon_name} ✨", Colours.BUFF))
    print(description)

    if boon_name == "Blessed Shrine":
        blessing_type = random.choice(["heal", "stat_boost", "temp_buff"])

        if blessing_type == "heal":
            # Use effective stats for accurate max health
            effective_stats = get_effective_stats(character, items_data)
            max_health = effective_stats["constitution"] * character["character"]["derived_stats"]["max_health"][
                "multiplier"]

            old_hp = character["character"]["current"]["health"]
            character["character"]["current"]["health"] = max_health
            healed = max_health - old_hp
            print(colourize(f"\n🌟 You are fully healed! +{healed} HP", Colours.HEAL))
            print(f"❤️ HP: {old_hp} → {max_health}")

        elif blessing_type == "stat_boost":
            stat = random.choice(["strength", "constitution", "intellect", "dexterity", "wisdom", "charisma"])
            boost = random.randint(1, 2)
            character["character"]["base_stats"][stat] += boost
            print(colourize(f"\n🌟 Your {stat.capitalize()} permanently increases by {boost}!", Colours.BUFF))

            # If constitution increased, update current health proportionally
            if stat == "constitution":
                effective_stats = get_effective_stats(character, items_data)
                new_max_health = effective_stats["constitution"] * \
                                 character["character"]["derived_stats"]["max_health"]["multiplier"]
                old_hp = character["character"]["current"]["health"]
                # Keep same percentage of health
                old_max = old_hp * 2  # Approximation, but better to store old max
                character["character"]["current"]["health"] = min(new_max_health, old_hp + boost * 2)
                print(f"❤️ HP adjusted to {character['character']['current']['health']}/{new_max_health}")

        else:  # temp_buff
            buffs = character["character"].setdefault("temp_buffs", {})
            buffs["blessing"] = {"amount": 5, "turns_remaining": 5}
            print(colourize(f"\n🌟 You receive a divine blessing! (+5 damage for 5 turns)", Colours.BUFF))

    elif boon_name == "Healing Light":
        # Use effective stats for accurate max health/mana
        effective_stats = get_effective_stats(character, items_data)
        max_health = effective_stats["constitution"] * character["character"]["derived_stats"]["max_health"][
            "multiplier"]
        max_mana = effective_stats["intellect"] * character["character"]["derived_stats"]["max_mana"]["multiplier"]

        old_hp = character["character"]["current"]["health"]
        old_mana = character["character"]["current"]["mana"]

        character["character"]["current"]["health"] = max_health
        character["character"]["current"]["mana"] = max_mana

        print(colourize(f"\n💚 You are fully restored!", Colours.HEAL))
        print(f"❤️ HP: {old_hp} → {max_health} (+{max_health - old_hp})")
        print(f"💙 Mana: {old_mana} → {max_mana} (+{max_mana - old_mana})")

    elif boon_name == "Ancient Knowledge":
        boost_type = random.choice(["xp", "intellect"])

        if boost_type == "xp":
            xp_gain = random.randint(25, 50)
            character["character"]["xp"] = character["character"].get("xp", 0) + xp_gain
            print(colourize(f"\n📚 You gained {xp_gain} XP from ancient knowledge!", Colours.XP))
        else:
            intellect_boost = random.randint(1, 3)
            character["character"]["base_stats"]["intellect"] += intellect_boost
            print(colourize(f"\n🧠 Your Intellect permanently increases by {intellect_boost}!", Colours.BUFF))

    return character


def handle_debuff(character: dict, event: dict) -> dict:
    """
    Handle debuff events - negative effects that hinder the character.

    Debuff types:
    - Poisonous Fog: Damage over time
    - Cursed Ground: Temporary stat reduction
    """
    debuff_name = event["name"]
    description = event["description"]

    print(colourize(f"\n☠️ {debuff_name} ☠️", Colours.DEBUFF))
    print(description)

    if debuff_name == "Poisonous Fog":
        # Instant damage + poison effect
        damage = random.randint(5, 15)
        character["character"]["current"]["health"] -= damage
        print(colourize(f"\n💀 You take {damage} damage from the poisonous fog!", Colours.FAIL))

        # Apply poison status effect
        statuses = character["character"].setdefault("status_effects", {})
        statuses["poison"] = {
            "active": True,
            "duration": 3,
            "damage_per_turn": 5
        }
        print(colourize(f"☠️ You are poisoned! (3 turns, 5 damage per turn)", Colours.DEBUFF))

        # Check if character died
        if character["character"]["current"]["health"] <= 0:
            print(colourize("\nThe poison proves fatal...", Colours.FAIL))

    elif debuff_name == "Cursed Ground":
        # Stat reduction debuff
        affected_stats = random.sample(["strength", "dexterity", "constitution"], k=2)
        debuff_amount = random.randint(2, 4)

        print(colourize(f"\n🌑 The curse drains your power!", Colours.DEBUFF))
        for stat in affected_stats:
            character["character"]["base_stats"][stat] -= debuff_amount
            print(colourize(f"   - {stat.capitalize()} decreased by {debuff_amount}", Colours.DEBUFF))

        # Store curse info for later restoration (optional - could be permanent for the floor)
        character["character"].setdefault("active_debuffs", {})
        character["character"]["active_debuffs"]["cursed_ground"] = {
            "stats": affected_stats,
            "amount": debuff_amount,
            "duration": 5  # Lasts for 5 turns
        }

    return character


def apply_status_effects(character: dict) -> dict:
    """
    Apply ongoing status effects (poison, etc.) at the start of combat or movement.
    """
    statuses = character["character"].get("status_effects", {})

    for status, data in list(statuses.items()):
        if data.get("active") and data.get("duration", 0) > 0:
            if status == "poison":
                damage = data.get("damage_per_turn", 5)
                character["character"]["current"]["health"] -= damage
                print(colourize(
                    f"☠️ Poison deals {damage} damage! ({character['character']['current']['health']} HP remaining)",
                    Colours.DEBUFF))

                data["duration"] -= 1
                if data["duration"] <= 0:
                    del statuses[status]
                    print(colourize("✨ The poison fades away.", Colours.HEAL))

    # Handle cursed ground duration
    debuffs = character["character"].get("active_debuffs", {})
    if "cursed_ground" in debuffs:
        debuffs["cursed_ground"]["duration"] -= 1
        if debuffs["cursed_ground"]["duration"] <= 0:
            # Restore stats
            curse = debuffs["cursed_ground"]
            for stat in curse["stats"]:
                character["character"]["base_stats"][stat] += curse["amount"]
            print(colourize("✨ The curse's hold on you weakens!", Colours.HEAL))
            del debuffs["cursed_ground"]

    return character