import random
import time

from game.progression import award_xp
from game.colours import Colours, colourize, hp_bar, mana_bar
from game.events import apply_status_effects
from game.character import get_effective_stats
from playsound3 import playsound
from itertools import cycle


def get_available_actions(character: dict, class_data: dict, cooldowns: dict) -> dict:
    """
    Retrieve the list of actions currently available to a character based on their class,
    level, and cooldown status.

    The function identifies the correct pathway from class_data by matching the character's
    class name. It then retrieves the actions available at the character's current level
    and filters out any actions that are still on cooldown.

    :param character: A dictionary containing character data, including class and level
    :param class_data: A dictionary containing all class/pathway definitions and actions
    :param cooldowns: A dictionary mapping action names to remaining cooldown turns
    :precondition: character contains valid "class" and "level" fields
                  class_data contains matching pathway and level data for the class
                  cooldowns maps action names to integers (0 means available)
    :postcondition: compute available actions
    :returns: A dictionary of actions that are currently available for use
    :raises ValueError: if no matching pathway is found for the character's class
    """
    character_class = character["character"]["class"]
    character_level = str(character["character"]["level"])

    pathway = None
    for pathway_data in class_data.values():
        if pathway_data["name"] == character_class:
            pathway = pathway_data
            break

    if pathway is None:
        raise ValueError(f"No pathway found for {character_class}.")

    actions = pathway["level"][character_level]["actions"]

    available_actions = {
        key: action
        for key, action in actions.items()
        if cooldowns.get(key, 0) == 0
    }

    return available_actions


def get_combat_command(character: dict, classes_data: dict, cooldowns: dict) -> tuple | None:
    """Display the combat menu and retrieve the player's chosen combat command."""
    available_actions = get_available_actions(character, classes_data, cooldowns)

    current_mana = character["character"]["current"]["mana"]
    current_health = character["character"]["current"]["health"]
    constitution = character["character"]["base_stats"]["constitution"]
    max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]
    intellect = character["character"]["base_stats"]["intellect"]
    max_mana = intellect * character["character"]["derived_stats"]["max_mana"]["multiplier"]


    print(f"\n--- {colourize(character['character']['name'], Colours.BOLD)} ---")
    print(f"❤️ HP:  {hp_bar(current_health, max_health)}")
    print(f"💙 Mana: {mana_bar(current_mana, max_mana)}")
    print("\nWhat will you do?")

    menu = {}
    index = 1
    for key, action in available_actions.items():
        mana_cost = action.get("mana_cost", 0)
        cooldown = action.get("cooldown", 0)
        cost_string = f"Mana: {mana_cost}" if mana_cost > 0 else ""
        cooldown_string = f"Cooldown: {cooldown}" if cooldown > 0 else ""


        action_type = action.get("type", "attack")
        if action_type == "attack":
            action_color = Colours.FAIL
        elif action_type == "heal":
            action_color = Colours.HEAL
        elif action_type == "buff":
            action_color = Colours.BUFF
        else:
            action_color = Colours.SPECIAL

        affordable = "" if current_mana >= mana_cost else f"{Colours.FAIL}Not enough mana.{Colours.ENDC}"

        print(f"{index}: {colourize(action['name'], action_color)} | {cost_string} {cooldown_string} {affordable}")

        menu[index] = ("action", key)
        index += 1

    print(f"{index}: {colourize('Items', Colours.CYAN)}")
    menu[index] = ("items", None)
    index += 1
    print(f"{index}: {colourize('Flee', Colours.WARNING)}")
    menu[index] = ("flee", None)

    while True:
        try:
            choice = int(input("\nEnter your choice: ").strip())
        except ValueError:
            print("Please enter an integer.")
            continue
        else:
            if choice in menu:
                choice_type, action_key = menu[choice]

                if choice_type == "action":
                    action = available_actions[action_key]
                    if current_mana < action.get("mana_cost", 0):
                        print(f"{Colours.FAIL}You don't have enough mana for {action['name']}!{Colours.ENDC}")
                        continue
                return choice_type, action_key
            else:
                print("Please enter a number corresponding to one of the options.")


def calculate_damage(character: dict, action: dict) -> int:
    """
    Calculate the total damage dealt by a character using a given action.

    The function computes damage based on the character's base stats and the
    scaling rules defined in the action. It supports both single-stat scaling
    (dictionary format) and multi-stat scaling (list format). After calculating
    base damage, any temporary buffs (such as attack boosts) are applied.

    :param character: A dictionary containing character data, including base stats
    :param action: A dictionary containing action data, including scaling rules
    :precondition: character contains valid "base_stats" with required stat keys
                   action contains a valid "scaling" field (dict or list of dicts)
    :postcondition: calculate damage to be done as an integer
    :returns: The total calculated damage as an integer
    """
    base_stats = character["character"]["base_stats"]
    scaling = action["scaling"]

    total_damage = 0
    if isinstance(scaling, list):
        for scale in scaling:
            stat_value = base_stats[scale["stat"]]
            total_damage += stat_value * scale["multiplier"]
    else:
        stat_value = base_stats[scaling["stat"]]
        total_damage += stat_value * scaling["multiplier"]

    temp_buffs = character["character"].get("temp_buffs", {})
    if "attack_boost" in temp_buffs:
        total_damage += temp_buffs["attack_boost"]["amount"]

    return int(total_damage)


def perform_action(character: dict, enemy: dict, action_key: str, action: dict, cooldowns: dict, items_data: dict) -> tuple | None:
    """
    Execute a combat action performed by the character against an enemy.

    Supports: attack, heal, buff, cleanse, status_effect types.
    """
    action_type = action["type"]
    fight_description = action.get("fight_description", f"You use {action['name']}.")
    mana_cost = action.get("mana_cost", 0)
    cooldown = action.get("cooldown", 0)

    # Apply mana cost
    character["character"]["current"]["mana"] -= mana_cost

    # Set cooldown if applicable
    if cooldown > 0:
        cooldowns[action_key] = cooldown

    print(f"{fight_description}")

    if action_type == "attack":
        damage = calculate_damage(character, action)
        enemy["health"] -= damage
        print(f"\033[91mYou deal {damage} damage!\033[0m The {enemy['name']} has {enemy['health']} HP remaining")


    elif action_type == "heal":
        amount = action.get("amount", 0)
        target = action.get("target", "self")
        # Calculate max health properly
        constitution = character["character"]["base_stats"]["constitution"]
        # Add trait bonuses

        for trait_bonus in character["character"].get("trait_bonuses", {}).values():
            if "constitution" in trait_bonus:
                constitution += trait_bonus["constitution"]

        max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]
        if target in ["self", "allies"]:
            old_hp = character["character"]["current"]["health"]
            # Can't heal above max health
            new_hp = min(old_hp + amount, max_health)
            actual_heal = new_hp - old_hp
            character["character"]["current"]["health"] = new_hp

            if actual_heal > 0:
                print(colourize(f"\n💚 {action['name']} heals for {actual_heal} HP!", Colours.HEAL))
                print(f"❤️ HP: {old_hp} → {new_hp}/{max_health}")
            else:
                print(
                    colourize(f"\n💚 {action['name']} attempts to heal, but you're already at full health!", Colours.HEAL))


    elif action_type == "buff":
        effect = action.get("effect", {})
        duration = effect.get("duration", 1)
        target = effect.get("target", "self")

        # Check for different types of buff effects

        if target in ["self", "allies"]:
            buffs = character["character"].setdefault("temp_buffs", {})
            # Handle damage reduction buff

            if "damage_reduction" in effect:
                reduction = effect["damage_reduction"]
                buff_key = "damage_reduction"
                buffs[buff_key] = {"amount": reduction, "turns_remaining": duration}

                print(colourize(f"\n🛡️ Your damage is reduced by {int(reduction * 100)}% for {duration} turns!",
                               Colours.BUFF))


            # Handle attack boost buff

            elif "attack_boost" in effect:
                boost = effect["attack_boost"]
                buff_key = "attack_boost"
                buffs[buff_key] = {"amount": boost, "turns_remaining": duration}

                print(colourize(f"\n⚔️ Your attack power increases by {boost} for {duration} turns!", Colours.BUFF))


            # Handle stat buff (like Song of Strength)

            elif "stat" in effect:
                stat = effect["stat"]
                amount = effect.get("amount", 0)
                buff_key = f"{stat}_boost"

                # For strength boosts, add to attack_boost for combat

                if stat == "strength":
                    buffs["attack_boost"] = {"amount": amount, "turns_remaining": duration}
                    print(colourize(f"\n💪 Your {stat.capitalize()} increases by {amount} for {duration} turns!",
                                   Colours.BUFF))

                else:
                    # Store generic stat buff
                    buffs[buff_key] = {"amount": amount, "turns_remaining": duration, "stat": stat}
                    print(colourize(f"\n✨ Your {stat.capitalize()} increases by {amount} for {duration} turns!",
                                   Colours.BUFF))

            # Handle taunt effect (Guardian Stance)
            elif effect.get("taunt"):
                buffs["taunt"] = {"active": True, "turns_remaining": duration}
                print(colourize(f"\n🛡️ You draw the enemy's attention for {duration} turns!", Colours.BUFF))

            # Handle counter stance
            elif effect.get("counter"):
                bonus_damage = effect.get("bonus_damage", 0)
                buffs["counter"] = {"active": True, "turns_remaining": duration, "bonus_damage": bonus_damage}
                print(colourize(f"\n⚔️ You prepare to counter the next attack for {duration} turns!", Colours.BUFF))


            # Handle status immunity (Sun Halo)
            elif effect.get("status_immunity"):
                buffs["status_immunity"] = {"active": True, "turns_remaining": duration}
                print(colourize(f"\n✨ You are immune to status effects for {duration} turns!", Colours.BUFF))

            # Handle barricade (scaling buff)

            elif "scaling" in action:
                scaling = action.get("scaling", {})

                if scaling:
                    stat = scaling.get("stat", "constitution")
                    multiplier = scaling.get("multiplier", 1)
                    stat_value = character["character"]["base_stats"].get(stat, 10)
                    reduction = min(0.5, stat_value * multiplier / 100)  # Cap at 50% reduction
                    buffs["damage_reduction"] = {"amount": reduction, "turns_remaining": duration}
                    print(colourize(
                        f"\n🛡️ You brace yourself, reducing damage by {int(reduction * 100)}% for {duration} turns!",
                        Colours.BUFF))

            else:
                # Generic buff message
                print(colourize(f"\n✨ You use {action['name']}!", Colours.BUFF))

    elif action_type == "cleanse":
        removes = action.get("removes", [])
        target = action.get("target", "self")

        if target in ["self", "allies"]:
            statuses = character["character"].get("status_effects", {})
            removed_any = False

            for status in removes:
                if status in statuses and statuses[status].get("active"):
                    del statuses[status]
                    removed_any = True

                    print(colourize(f"\n✨ {status.capitalize()} has been cleansed!", Colours.HEAL))

            if not removed_any:
                print(colourize(f"\n✨ No status effects to cleanse.", Colours.HEAL))

    elif action_type == "status_effect":
        effect = action.get("effect", {})
        effect_type = effect.get("type")
        chance = effect.get("chance", 1.0)
        duration = effect.get("duration", 1)
        target = effect.get("target", "enemies")

        if target in ["enemies", "enemy"] and random.random() < chance:
            # Apply status effect to enemy
            enemy_statuses = enemy.setdefault("status_effects", {})

            if effect_type == "blind":
                enemy_statuses[effect_type] = {"active": True, "duration": duration}
                print(colourize(f"\n🌑 The {enemy['name']} is blinded for {duration} turns!", Colours.DEBUFF))


            elif effect_type == "slow":
                enemy_statuses[effect_type] = {"active": True, "duration": duration, "damage_reduction": 0.3}
                print(colourize(f"\n🐌 The {enemy['name']} is slowed for {duration} turns!", Colours.DEBUFF))


            elif effect_type == "weakness":
                enemy_statuses[effect_type] = {"active": True, "duration": duration, "damage_reduction": 0.2}
                print(colourize(f"\n💪 The {enemy['name']} is weakened for {duration} turns!", Colours.DEBUFF))


            elif effect_type == "corruption":
                enemy_statuses[effect_type] = {"active": True, "duration": duration, "confusion": True}
                print(colourize(f"\n🌑 The {enemy['name']} is corrupted for {duration} turns!", Colours.DEBUFF))


            elif effect_type == "stun":
                enemy_statuses[effect_type] = {"active": True, "duration": duration}
                print(colourize(f"\n💫 The {enemy['name']} is stunned for {duration} turns!", Colours.DEBUFF))


            else:
                # Generic status effect
                enemy_statuses[effect_type] = {"active": True, "duration": duration}
                print(colourize(f"\n✨ The {enemy['name']} is affected by {effect_type} for {duration} turns!", Colours.DEBUFF))

    else:
        print(colourize(f"\n❌ The status effect failed to apply!", Colours.FAIL))

    return enemy, cooldowns


def tick_cooldowns(cooldowns: dict) -> dict:
    """
    Decrease all active cooldown values by one turn and remove expired cooldowns.

    The function iterates through a dictionary of cooldowns, reducing each value by 1.
    Any cooldown that reaches 0 or below is removed from the returned dictionary.

    :param cooldowns: A dictionary mapping action names to remaining cooldown turns
    :precondition: cooldowns contains action names as keys and positive integers as values
    :postcondition: reduce all cooldown values by 1 and remove expired cooldowns
    :returns: A new dictionary containing only active cooldowns with updated values
    """
    updated_cooldowns = {}

    for key, turns in cooldowns.items():
        if turns - 1 > 0:
            updated_cooldowns[key] = turns - 1

    return updated_cooldowns


def tick_temp_buffs(character: dict) -> dict:
    """
    Decrease the duration of temporary buffs on a character and remove expired buffs.

    The function iterates through all active temporary buffs, reducing their remaining
    turn duration by 1. If a buff's duration reaches zero or below, it is removed from
    the character and a message is printed indicating that the buff has expired.

    :param character: A dictionary containing character data, including optional "temp_buffs"
    :precondition: If present, "temp_buffs" is a dictionary where each buff contains a
                  "turns_remaining" integer value
    :postcondition: reduce all buff durations by 1 and remove expired buffs
    :returns: The updated character dictionary with modified temporary buffs
    """
    buffs = character["character"].get("temp_buffs", {})
    expired = []

    for buff_key, buff in buffs.items():
        buff["turns_remaining"] -= 1
        if buff["turns_remaining"] <= 0:
            expired.append(buff_key)
            print(f"Your {buff_key.replace('_', ' ')} has worn off")

    for key in expired:
        del buffs[key]

    return character


def display_inventory(character: dict) -> None:
    """
    Display all consumable items in the character's inventory.

    The function filters the character's inventory to show only items of type
    "consumable". If no consumable items exist, a message is printed. Otherwise,
    it prints a numbered list of all consumable items.

    :param character: A dictionary containing character data, including an "inventory"
                      list under the "character" key
    :precondition: character["character"]["inventory"] exists and is a list of
                   dictionaries containing at least "name" and "type" keys
    :postcondition: print consumable items to the console in numbered order,
                    or print a message if none exist
    :returns: None
    """
    inventory = character["character"]["inventory"]
    consumables = [item for item in inventory if item["type"] == "consumable"]

    if len(consumables) == 0:
        print("You have no consumable items!")
        return

    print("Inventory:")
    for index, item in enumerate(consumables, 1):
        print(f"{index}: {item['name']}")

    return


def use_item(character: dict, enemy: dict, items_data: dict) -> tuple | None:
    """
    Allow the player to use a consumable item from their inventory during combat.
    """
    inventory = character["character"]["inventory"]
    consumables = [item for item in inventory if item["type"] == "consumable"]

    if len(consumables) == 0:
        print("You have no consumable items!")
        return character, enemy

    display_inventory(character)

    while True:
        try:
            choice = int(input("Choose an item (0 to cancel): ").strip())
        except ValueError:
            print("Please enter an integer.")
            continue
        else:
            if choice == 0:
                print("You put your bag away.")
                return character, enemy
            elif 1 <= choice <= len(consumables):
                item = consumables[choice - 1]
                character, enemy = apply_item_effect(character, item, enemy, items_data)
                inventory.remove(item)

                return character, enemy
            else:
                print("Please enter a number corresponding to one of the options.")


def apply_item_effect(character: dict, item: dict, enemy: dict, items_data: dict) -> tuple:
    """
    Apply the effects of a consumable item to the character and/or enemy.
    """
    effect = item["effect"]
    name = item["name"]

    # Get max health properly
    effective_stats = get_effective_stats(character, items_data)

    max_health = effective_stats["constitution"] * character["character"]["derived_stats"]["max_health"]["multiplier"]
    max_mana = effective_stats["intellect"] * character["character"]["derived_stats"]["max_mana"]["multiplier"]

    if "heal" in effect:
        current_health = character["character"]["current"]["health"]
        heal_amount = effect["heal"]

        # Calculate actual healing (can't exceed max health)
        actual_heal = min(heal_amount, max_health - current_health)
        character["character"]["current"]["health"] += actual_heal

        print(colourize(f"\n💚 You use {name} and gain {actual_heal} HP!", Colours.HEAL))
        print(f"❤️ HP: {current_health} → {character['character']['current']['health']}/{max_health}")

    if "damage" in effect:
        target = effect.get("target", "enemy")
        damage = effect["damage"]
        duration = effect.get("duration", 0)

        if target == "enemy" and enemy is not None:
            enemy["health"] -= damage
            if duration > 0:
                print(colourize(
                    f"\n💥 You use {name}! The {enemy['name']} takes {damage} damage per turn for {duration} turns.",
                    Colours.FAIL))
                # Add damage over time effect to enemy
                enemy.setdefault("status_effects", {})
                enemy["status_effects"]["burn"] = {
                    "active": True,
                    "duration": duration,
                    "damage_per_turn": damage
                }
                print(f"{enemy['name']} has {enemy['health']} HP remaining.")
            else:
                print(colourize(f"\n💥 You use {name}! The {enemy['name']} takes {damage} damage.", Colours.FAIL))
                print(f"{enemy['name']} has {enemy['health']} HP remaining.")
        elif target == "self":
            character["character"]["current"]["health"] -= damage
            print(colourize(f"\n💀 You use {name}! You take {damage} damage.", Colours.FAIL))
            print(f"❤️ HP: {character['character']['current']['health']}/{max_health}")

    if "xp" in effect:
        character["character"]["pending_xp"] = character["character"].get("pending_xp", 0) + effect["xp"]
        print(colourize(f"\n📚 You use {name} and gain {effect['xp']} XP!", Colours.XP))

    if "attack_boost" in effect:
        duration = effect.get("duration", 1)
        boost = effect["attack_boost"]
        buffs = character["character"].setdefault("temp_buffs", {})
        buffs["attack_boost"] = {"amount": boost, "turns_remaining": duration}
        print(
            colourize(f"\n⚔️ You use {name}! Your attack power increases by {boost} for {duration} turns.", Colours.BUFF))

    return character, enemy


def flee(character: dict) -> bool:
    """
    Attempt to flee from combat with a 50% success rate.

    The function generates a random value to determine whether the character
    successfully escapes from combat. If the value is 0.5 or higher, the flee
    attempt succeeds; otherwise, it fails.

    :param character: A dictionary containing character data, including the
                      character's name under "character" -> "name"
    :precondition: character must contain "character" and "name" keys
    :postcondition: print a message indicating success or failure of fleeing
    :returns: True if the character successfully flees, False otherwise
    """
    chance = random.random()

    if chance >= 0.5:
        print(f"{character['character']['name']} successfully fled from combat!")
        return True
    else:
        print("You failed to flee!")
        return False


def enemy_behaviour(character: dict, enemy: dict) -> dict:
    """
    Execute the enemy's turn with status effect handling.
    """
    # Process enemy status effects first
    if "status_effects" in enemy:
        for status, data in list(enemy["status_effects"].items()):
            if data.get("active"):
                if status == "stun":
                    print(colourize(f"\n💫 The {enemy['name']} is stunned and cannot act!", Colours.DEBUFF))
                    data["duration"] = data.get("duration", 1) - 1
                    if data["duration"] <= 0:
                        del enemy["status_effects"][status]
                    return character

                elif status == "blind":
                    # 50% chance to miss when blinded
                    if random.random() < 0.5:
                        print(colourize(f"\n🌑 The {enemy['name']} is blinded and misses!", Colours.DEBUFF))
                        data["duration"] = data.get("duration", 1) - 1
                        if data["duration"] <= 0:
                            del enemy["status_effects"][status]
                        return character

                elif status == "slow":
                    print(colourize(f"\n🐌 The {enemy['name']} is slowed and attacks weakly!", Colours.DEBUFF))
                    # Slowed enemies deal less damage (handled in attack calculation)

                elif status == "weakness":
                    print(colourize(f"\n💪 The {enemy['name']} is weakened!", Colours.DEBUFF))

                elif status == "poison":
                    poison_damage = data.get("damage_per_turn", 5)
                    character["character"]["current"]["health"] -= poison_damage
                    print(colourize(f"\n☠️ Poison deals {poison_damage} damage to {enemy['name']}!", Colours.DEBUFF))
                    data["duration"] = data.get("duration", 1) - 1
                    if data["duration"] <= 0:
                        del enemy["status_effects"][status]
                    # Don't return - enemy still attacks this turn

                elif status == "burn":
                    burn_damage = data.get("damage_per_turn", 5)
                    character["character"]["current"]["health"] -= burn_damage
                    print(colourize(f"\n🔥 Burn deals {burn_damage} damage to {enemy['name']}!", Colours.DEBUFF))
                    data["duration"] = data.get("duration", 1) - 1
                    if data["duration"] <= 0:
                        del enemy["status_effects"][status]

                # Update duration for other status effects
                elif "duration" in data:
                    data["duration"] -= 1
                    if data["duration"] <= 0:
                        del enemy["status_effects"][status]

    # Calculate damage with any active debuffs on enemy
    chosen_attack = random.choice(enemy["attacks"])
    damage = chosen_attack["damage"]
    description = chosen_attack["description"]

    # Apply enemy debuffs to damage
    if "status_effects" in enemy:
        if "weakness" in enemy["status_effects"]:
            damage = int(damage * 0.8)
        if "slow" in enemy["status_effects"]:
            damage = int(damage * 0.7)

    character["character"]["current"]["health"] -= damage
    print(colourize(f"\n{description}", Colours.FAIL))
    print(colourize(f"💥 You take {damage} damage!", Colours.FAIL))

    # Get max health for display
    constitution = character["character"]["base_stats"]["constitution"]
    for trait_bonus in character["character"].get("trait_bonuses", {}).values():
        if "constitution" in trait_bonus:
            constitution += trait_bonus["constitution"]


    return character

    # Normal enemy attack
    chosen_attack = random.choice(enemy["attacks"])
    damage = chosen_attack["damage"]
    description = chosen_attack["description"]

    character["character"]["current"]["health"] -= damage
    print(f"\n{description}")
    print(f"\033[91mYou take {damage} damage!\033[0m")
    print(f"You have {character['character']['current']['health']} HP remaining.")
    return character


def combat(character: dict, events_by_id: dict, atlas: dict, class_data: dict, items_data) -> bool:
    """
    Run a full combat encounter between the player and an enemy at the character's current location.

    The function retrieves the enemy from the map (atlas + event data), then enters a turn-based
    combat loop where the player can perform actions, use items, or attempt to flee. After each
    player turn, the enemy may act. The system also manages cooldowns, temporary buffs, XP rewards,
    and victory/defeat conditions.

    :param character: A dictionary containing the player character state, including stats, location,
                      health, mana, inventory, and class data
    :param events_by_id: A dictionary mapping event IDs to event data including enemy definitions
    :param atlas: A multi-layer map structure containing event IDs at each coordinate position
    :param class_data: Class/pathway data used for available actions and scaling abilities
    :param items_data: Item database used for consumables and equipment effects
    :precondition: character must contain valid location, stats, and current health/mana values
    :precondition: atlas coordinates must map to valid event IDs in events_by_id
    :precondition: enemy data must contain at least "name" and "health"
    :postcondition: Character and enemy states are modified through combat until one is defeated
    :returns: True if the player wins or successfully flees, False if the player is defeated
    """
    sound = playsound("sounds/clavar_la_espada_shiro_sagisu.mp3", block=False)
    songs = [
        "sounds/la_distancia_para_un_duelo_shiro_sagisu.mp3",
        "sounds/principio_de_lucha_shiro_sagisu.mp3",
        "sounds/clavar_la_espada_shiro_sagisu.mp3"
    ]
    playlist = cycle(songs)

    xp_rewards = {
        "Bandit": 25,
        "Beast": 30,
        "Skeleton": 20
    }

    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    event_id = atlas[character_z]["position"][(character_y, character_x)]
    event = events_by_id[event_id]
    enemy = dict(event["enemy"])

    cooldowns = {}

    print(f"A {enemy['name']} appears!")

    while enemy["health"] > 0 and character["character"]["current"]["health"] > 0:
        character = apply_status_effects(character)

        if character["character"]["current"]["health"] <= 0:
            print(colourize(f"\n{character['character']['name']} has been defeated by lingering effects!", Colours.FAIL))
            sound.stop()
            return False

        if not sound.is_alive():
            sound = playsound(next(playlist), block=False)

        choice_type, action_key = get_combat_command(character, class_data, cooldowns)

        enemy_turn = False

        if choice_type == "action":
            action = get_available_actions(character, class_data, cooldowns)[action_key]
            enemy, cooldowns = perform_action(character, enemy, action_key, action, cooldowns, items_data)

            if enemy["health"] <= 0:
                print(f"You defeated the {enemy['name']}!")
                xp = xp_rewards.get(enemy["name"], 10)
                character = award_xp(character, xp, class_data, items_data)
                sound.stop()
                return True
            enemy_turn = True

        elif choice_type == "items":
            character, enemy = use_item(character, enemy, items_data)
            if enemy is not None and enemy["health"] <= 0:
                print(f"\nYou defeated the {enemy['name']}!")
                xp = xp_rewards.get(enemy["name"], 10)
                character = award_xp(character, xp, class_data, items_data)
                sound.stop()
                return True
            enemy_turn = False

        elif choice_type == "flee":
            if flee(character):
                sound.stop()
                return True
            enemy_turn = True

        if enemy_turn:
            character = enemy_behaviour(character, enemy)
            cooldowns = tick_cooldowns(cooldowns)
            character = tick_temp_buffs(character)

            if character["character"]["current"]["health"] <= 0:
                print(f"\n{character['character']['name']} has been defeated!")
                sound.stop()
                return False
    sound.stop()
    return False


def boss_combat(character: dict, boss_enemy: dict, class_data: dict, items_data: dict) -> bool:
    """
    Run a boss combat encounter between the player and a final boss enemy.

    This function manages a turn-based combat loop similar to regular combat, but
    with special boss rules (e.g., fleeing is disabled). The player can perform
    actions or use items while cooldowns and temporary buffs are tracked. The boss
    acts after the player's turn when applicable. The fight continues until either
    the boss or the player is defeated.

    :param character: A dictionary containing the player character state, including
                      stats, inventory, current health/mana, and class data
    :param boss_enemy: A dictionary representing the boss enemy, including at least
                       "name" and "health"
    :param class_data: Class/pathway data used for available actions and scaling abilities
    :param items_data: Item database used for consumable effects
    :precondition: character must contain valid stats, location, and current health/mana
    :precondition: boss_enemy must contain valid "name" and "health" keys
    :precondition: class_data must match the character's class structure
    :postcondition: The boss fight modifies character and boss state until one is defeated
    :returns: True if the player defeats the boss, False if the player is defeated
    """
    sound = playsound("sounds/escalon_shiro_sagisu.mp3", block=False)

    cooldowns = {}

    if "original_player_name" in boss_enemy:
        original_name = boss_enemy["original_player_name"]
        original_class = boss_enemy.get("original_class", "Unknown")
        original_level = boss_enemy.get("original_level", 1)

        print(colourize(f"\n{'=' * 60}", Colours.TITLE))
        print(colourize(f"⚠️  THE CORRUPTED SHADOW OF {original_name.upper()}  ⚠️", Colours.FAIL))
        print(colourize(f"{'=' * 60}", Colours.TITLE))
        print(f"\nA dark, twisted version of {original_name} stands before you.")
        print(f"Once a level {original_level} {original_class}, they have been corrupted by the dungeon's power.")
        print(f"Their techniques have been twisted into dark reflections of their former glory.")
        print(colourize(f"\n\"I remember you... but I cannot stop...\"", Colours.DEBUFF))
        print(f"\nTo escape, you must put their soul to rest...")
    else:
        print(colourize(f"\n{'=' * 50}", Colours.TITLE))
        print(colourize(f"BOSS ENCOUNTER: {boss_enemy['name']}", Colours.FAIL))
        print(colourize(f"{'=' * 50}", Colours.TITLE))

        # Add a dramatic pause
    time.sleep(2)

    while boss_enemy["health"] > 0 and character["character"]["current"]["health"] > 0:
        if not sound.is_alive():
            sound = playsound("sounds/escalon_shiro_sagisu.mp3", block=False)
        choice_type, action_key = get_combat_command(character, class_data, cooldowns)

        enemy_turn = False

        if choice_type == "action":
            action = get_available_actions(character, class_data, cooldowns)[action_key]
            boss_enemy, cooldowns = perform_action(character, boss_enemy, action_key, action, cooldowns, items_data)

            if boss_enemy["health"] <= 0:
                print(f"You defeated the {boss_enemy['name']}!")
                return True
            enemy_turn = True

        elif choice_type == "items":
            character, boss_enemy = use_item(character, boss_enemy, items_data)
            if boss_enemy is not None and boss_enemy["health"] <= 0:
                print(f"You defeated the {boss_enemy['name']}!")
                return True
            enemy_turn = False

        elif choice_type == "flee":
            print("You cannot flee from a boss!")
            enemy_turn = False

        if enemy_turn and character["character"]["current"]["health"] > 0:
            character = enemy_behaviour(character, boss_enemy)
            cooldowns = tick_cooldowns(cooldowns)
            character = tick_temp_buffs(character)

            if character["character"]["current"]["health"] <= 0:
                print(f"{character['character']['name']} has been defeated!")
                return False

    return False


def main():
    return


if __name__ == '__main__':
    main()
