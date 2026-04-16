import random


def get_available_actions(character: dict, class_data: dict, cooldowns: dict) -> dict:
    character_class = character["character"]["class"]
    character_level = character["character"]["level"]

    pathway = None
    for pathway_key, pathway_data in class_data.items():
        if pathway_data["name"] == character_class or any(level_data["name"] == character_class
                                                          for level_data in pathway_data["levels"].values()):
            pathway = pathway_data
            break

    if pathway is None:
        raise ValueError(f"No pathway found for {character_class}.")

    actions = pathway["level"][character_level]["actions"]

    available_actions = {key: action for key, action in actions.items() if cooldowns.get(key, 0) == 0}

    return available_actions


def get_combat_command(character: dict, classes_data: dict, cooldowns: dict) -> tuple | None:
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

        menu[index] = action
        index += 1

    print(f"{index}: Items")
    menu[index] = ("items", None)
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
    updated_cooldowns = {}

    for key, turns in cooldowns.items():
        if turns - 1 > 0:
            updated_cooldowns[key] = turns - 1

    return updated_cooldowns


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


def use_item(character: dict) -> dict | None:
    inventory = character["character"]["inventory"]
    consumables = [item for item in inventory if item["type"] == "consumable"]

    if len(consumables) == 0:
        print("You have no consumable items!")
        return character

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
                return character
            elif 1 <= choice <= len(consumables):
                item = consumables[choice - 1]
                character = apply_item_effect(character, item)
                inventory.remove(item)
                return character
            else:
                print("Please enter a number corresponding to one of the options.")


def apply_item_effect(character: dict, item: dict) -> dict:
    effect = item["effect"]
    name = item["name"]

    if "health" in effect:
        constitution = character["character"]["base_stats"]["constitution"]
        max_health = constitution * character["character"]["derived_stats"]["max_health"]["multiplier"]
        current_health = character["character"]["current"]["health"]
        healed = effect["heal"], max_health - current_health
        character["character"]["current"]["health"] += healed

        print(f"You use {name} and recover {healed} HP!")
        print(f"Current HP: {current_health}/{max_health}")

    return character


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



def combat(character: dict, events_by_id: dict, atlas: dict, classes_data: dict) -> bool:
    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    event_id = atlas[character_z]["position"][(character_y, character_x)]
    event = events_by_id[event_id]
    enemy = dict(event["enemy"])

    cooldowns = {}

    print(f"A {enemy['name']} appears!")

    while enemy["health"] > 0 and character["character"]["current"]["health"] > 0:
        choice_type, action_key = get_combat_command(character, classes_data, cooldowns)

        enemy_turn = False

        if choice_type == "action":
            action = get_available_actions(character, classes_data, cooldowns)[action_key]
            enemy, cooldowns = perform_action(character, enemy, action_key, action, cooldowns)

            if enemy["health"] <= 0:
                print(f"You defeated the {enemy['name']}!")
                return True
            enemy_turn = True

        elif choice_type == "items":
            use_item(character)
            enemy_turn = False

        elif choice_type == "flee":
            if flee(character):
                return True
            enemy_turn = True

        if enemy_turn:
            character = enemy_behaviour(character, enemy)
            cooldowns = tick_cooldowns(cooldowns)

            if character["character"]["current"]["health"] <= 0:
                print(f"{character['character']['name']} has been defeated!")
                return False

    return False


def boss_behaviour():
    pass


def main():
    return


if __name__ == '__main__':
    main()