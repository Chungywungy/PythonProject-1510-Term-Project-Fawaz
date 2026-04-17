import random
from game.character import award_xp

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
    """
    Display the combat menu and retrieve the player's chosen combat command.

    The function builds a list of available actions based on the character's class,
    level, mana, and cooldown status. It then presents a menu including actions,
    items, and flee options, and prompts the user to select an option.

    If an action is selected, the function checks whether the character has enough
    mana before confirming the choice.

    :param character: A dictionary containing character stats, current health, mana,
                      and base/derived attributes
    :param classes_data: A dictionary containing class definitions, levels, and actions
    :param cooldowns: A dictionary mapping action names to remaining cooldown values
    :precondition: character contains valid "base_stats", "derived_stats", and "current"
                   classes_data contains valid actions for the character's class and level
                   cooldowns maps action keys to integers (0 = available)
    :postcondition: print a menu and prompt the user until a valid choice is made
    :returns: A tuple in the form (choice_type, action_key) where:
              - choice_type is "action", "items", or "flee"
              - action_key is the selected action key or None for non-action choices
    """
    available_actions = get_available_actions(character, classes_data, cooldowns)

    current_mana = character["character"]["current"]["mana"]
    current_health = character["character"]["current"]["health"]
    constitution = character["character"]["base_stats"]["constitution"]
    max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]

    print(f"--- {character['character']['name']} | HP: {current_health}/{max_health} | mana: {current_mana} ---")
    print("What will you do?")

    menu = {}
    index = 1
    for key, action in available_actions.items():
        mana_cost = action.get("mana_cost", 0)
        cooldown = action.get("cooldown", 0)
        cost_string = f"Mana: {mana_cost}" if mana_cost > 0 else ""
        cooldown_string = f"Cooldown: {cooldown}" if cooldown > 0 else ""
        affordable = "" if current_mana >= mana_cost else "Not enough mana."

        print(f"{index}: {action['name']} | {cost_string}{cooldown_string}{affordable}")

        menu[index] = ("action", key)
        index += 1

    print(f"{index}: Items")
    menu[index] = ("items", None)
    index += 1
    print(f"{index}: Flee")
    menu[index] = ("flee", None)

    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter an integer.")
            continue
        else:
            if choice in menu:
                choice_type, action_key = menu[choice]

                if choice_type == "action":
                    action = available_actions[action_key]
                    if current_mana < action.get("mana_cost", 0):
                        print(f"You don't have enough mana for {action}!")
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


def perform_action(character: dict, enemy: dict, action_key: str, action: dict, cooldowns: dict) -> tuple | None:
    """
    Execute a combat action performed by the character against an enemy.

    The function applies the effects of the selected action, including mana cost,
    cooldown assignment, and damage calculation for attack-type actions. It also
    prints a combat description and updates both the enemy's health and cooldown state.

    If the action type is not implemented, a placeholder message is displayed.

    :param character: A dictionary containing character stats and current resources
    :param enemy: A dictionary representing the enemy, including health and name
    :param action_key: The identifier of the action being performed
    :param action: A dictionary containing action metadata (type, cost, scaling, etc.)
    :param cooldowns: A dictionary tracking cooldown values for actions
    :precondition: character contains valid "current" mana values
                  enemy contains "health" and "name"
                  action contains valid "type" and optional combat fields
    :postcondition: enemy health may be reduced, character mana is reduced,
                   cooldowns may be updated, and messages are printed
    :returns: A tuple (enemy, cooldowns) after the action is applied
    """
    action_type = action["type"]
    fight_description = action.get("fight_description", f"You use {action['name']}.")
    mana_cost = action.get("mana_cost", 0)
    cooldown = action.get("cooldown", 0)

    character["character"]["current"]["mana"] -= mana_cost

    if cooldown > 0:
        cooldowns[action_key] = cooldown

    print(f"{fight_description}")

    if action_type == "attack":
        damage = calculate_damage(character, action)
        enemy["health"] -= damage
        print(f"You deal {damage} damage! The {enemy['name']} has {enemy['health']} HP remaining")
    else:
        print(f"Effect not implemented yet for type: {action_type}")

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
    inventory = character["character"]["inventory"]
    consumables = [item for item in inventory if item["type"] == "consumable"]

    if len(consumables) == 0:
        print("You have no consumable items!")
        return

    print("Inventory:")
    for index, item in enumerate(consumables, 1):
        print(f"{index}: {item['name']}")

    return


def use_item(character: dict, enemy: dict) -> tuple | None:
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
                character = apply_item_effect(character, item, enemy)
                inventory.remove(item)

                return character, enemy
            else:
                print("Please enter a number corresponding to one of the options.")


def apply_item_effect(character: dict, item: dict, enemy: dict) -> tuple:
    effect = item["effect"]
    name = item["name"]

    constitution = character["character"]["base_stats"]["constitution"]
    max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]

    if "heal" in effect:
        current_health = character["character"]["current"]["health"]
        healed = min(effect["heal"], max_health) - current_health
        character["character"]["current"]["health"] += healed

        print(f"You use {name} and recover {healed} HP!")
        print(f"Current HP: {current_health}/{max_health}")

    if "damage" in effect:
        target = effect.get("target", "enemy")
        damage = effect["damage"]
        duration = effect.get("duration", 0)

        if target == "enemy" and enemy is not None:
            enemy["health"] -= damage
            if duration > 0:
                print(f"You use {name}! The {enemy['name']} takes {damage} damage per turn for {duration} turns.\n"
                      f"{enemy['name']} has {enemy['health']} HP remaining.")
            else:
                print(f"You use {name}! The {enemy['name']} takes {damage} damage.\n"
                      f"{enemy['name']} has {enemy['health']} HP remaining.")
        elif target == "self":
            character["character"]["current"]["health"] -= damage
            print(f"You use {name}! You take {damage} damage.\n"
                  f"You have {character['character']['current']['health']} HP remaining.")

    if "xp" in effect:
        character["character"]["pending_xp"] = character["character"].get("pending_xp", 0) + effect["xp"]

        print(f"You use {name} and gain {effect['xp']} xp!")

    if "attack_boost" in effect:
        duration = effect.get("duration", 1)
        boost = effect["attack_boost"]
        buffs = character["character"].setdefault("temp_buffs", {})
        buffs["attack_boost"] = {"amount": boost, "turns_remaining": duration}

        print(f"You use {name}! Your attack power increases by {boost} for {duration} turns.")

    return character, enemy


def flee(character: dict) -> bool:
    chance = random.random()

    if chance >= 0.5:
        print(f"{character['character']['name']} successfully fled from combat!")
        return True
    else:
        print("You failed to flee!")
        return False


def enemy_behaviour(character: dict, enemy: dict) -> dict:
    chosen_attack = random.choice(enemy["attacks"])
    damage = chosen_attack["damage"]
    description = chosen_attack["description"]


    character["character"]["current"]["health"] -= damage
    print(f"{description}\nYou take {damage} damage!\n"
          f"You have {character["character"]["current"]["health"]} HP remaining.")
    return character



def combat(character: dict, events_by_id: dict, atlas: dict, class_data: dict, items_data) -> bool:
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
        choice_type, action_key = get_combat_command(character, class_data, cooldowns)

        enemy_turn = False

        if choice_type == "action":
            action = get_available_actions(character, class_data, cooldowns)[action_key]
            enemy, cooldowns = perform_action(character, enemy, action_key, action, cooldowns)

            if enemy["health"] <= 0:
                print(f"You defeated the {enemy['name']}!")
                xp = xp_rewards.get(enemy["name"], 10)
                character = award_xp(character, xp, class_data, items_data)
                return True
            enemy_turn = True

        elif choice_type == "items":
            character, enemy = use_item(character, enemy)
            if enemy is not None and enemy["health"] <= 0:
                print(f"You defeated the {enemy['name']}!")
                xp = xp_rewards.get(enemy["name"], 10)
                character = award_xp(character, xp, class_data, items_data)
                return True
            enemy_turn = False

        elif choice_type == "flee":
            if flee(character):
                return True
            enemy_turn = True

        if enemy_turn:
            character = enemy_behaviour(character, enemy)
            cooldowns = tick_cooldowns(cooldowns)
            character = tick_temp_buffs(character)

            if character["character"]["current"]["health"] <= 0:
                print(f"{character['character']['name']} has been defeated!")
                return False

    return False


def boss_combat(character: dict, boss_enemy: dict, class_data: dict, items_data: dict) -> bool:
    cooldowns = {}

    print(f"A {boss_enemy['name']} appears! This is the final challenge!")

    while boss_enemy["health"] > 0 and character["character"]["current"]["health"] > 0:
        choice_type, action_key = get_combat_command(character, class_data, cooldowns)

        enemy_turn = False

        if choice_type == "action":
            action = get_available_actions(character, class_data, cooldowns)[action_key]
            boss_enemy, cooldowns = perform_action(character, boss_enemy, action_key, action, cooldowns)

            if boss_enemy["health"] <= 0:
                print(f"You defeated the {boss_enemy['name']}!")
                return True
            enemy_turn = True

        elif choice_type == "items":
            character, boss_enemy = use_item(character, boss_enemy)
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