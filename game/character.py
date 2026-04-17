from game.file_tampering import open_json


def character_name() -> str:
    """
    Prompt the user to input and confirm a character name.

    The function asks the user to enter a name, formats it, and then
    requests confirmation. If no name is provided, the user is prompted
    to accept a default name ("Amon") or re-enter a name. The process
    repeats until a valid confirmation is received.

    :param: None
    :precondition: the user is able to provide input via the console
    :postcondition: valid character name is returned as a string
    :returns: the confirmed character name as a string
    """
    mc_name = str(input("What is your characters' name? ").strip().title())

    while True:
        if len(mc_name) == 0:
            validate = str(input("The default name is Amon. Are you sure about your choice? (y/n) ")).strip().lower()
            if validate == 'y':
                mc_name = 'Amon'
                break
            elif validate == 'n':
                mc_name = str(input("What is your characters' name? ").strip().title())
                continue
            else:
                print("Please input 'y' or 'n'.")
                continue
        else:
            validate = str(
                input(f"Your character's name is {mc_name}. Are you sure about that? (y/n) ")).strip().lower()
            if validate == 'y':
                break
            elif validate == 'n':
                mc_name = str(input("What is your characters' name? ").strip().title())
                continue
            else:
                print("Please input 'y' or 'n'.")
                continue
    return mc_name


def player_name() -> str:
    """
    Prompt the user to input and confirm their player name.

    The function asks the user to enter their name and ensures that it is
    not empty. The user must then confirm their input. If the name is empty
    or not confirmed, the user is repeatedly prompted until a valid and
    confirmed name is provided.

    :param: None
    :precondition: the user is able to provide input via the console
    :postcondition: valid player name is returned as a string
    :returns: the confirmed player name as a string
    """
    player = str(input("What is your name oh mighty player? ")).strip().title()

    while True:
        if len(player) == 0:
            player = str(input("You can't have no name. Now tell me what is your name? ")).strip().title()
            continue
        else:
            validate = str(
                input(f"Your name is {player}. Are you sure about that? (y/n) ")).strip().lower()
            if validate == 'y':
                break
            elif validate == 'n':
                player = str(input("What is your name, player? ").strip().title())
                continue
            else:
                print("Please input 'y' or 'n'.")
                continue
    return player


def character_class(file: str):
    class_data = open_json(file)

    pathway_names = {data["name"]: key for key, data in class_data.items()}


    while True:
        pick_class = str(input("What is your character's pathway? ")).strip().title()
        print("Available pathways: "+", ".join(pathway_names.keys()))

        if len(pick_class) == 0:
           print("your character's pathway can't be empty.")
           continue
        if pick_class not in pathway_names:
            print(f"{pick_class} is not a valid pathway. Please choose from the list of available pathways.")
            continue

        print(f"")
        validate = str(input(f"your character will follow the {pick_class} pathway.\n"
                             f"Are you sure about that? (y/n) ")).strip().lower()

        if validate == 'y':
            break
        elif validate == 'n':
            continue
        else:
            print("Please input 'y' or 'n'.")

    return pick_class


def get_effective_stats(character:dict, items_data: dict) -> dict:
    base = dict(character["character"]["base_stats"])
    effective = dict(base)

    for trait_bonus in character["character"].get("trait_bonuses", {}).values():
        for stat, amount in trait_bonus.items():
            if stat in effective:
                effective[stat] += amount

    items_by_name = {item["name"]: item for item in items_data["items"] if item["type"] == "equipment"}

    for slot, item_name in character["character"]["equipment"].items():
        if item_name and item_name in items_by_name:
            for stat, amount in items_by_name[item_name]["stats"].items():
                if stat in effective:
                    effective[stat] += amount

    return effective


def apply_class_traits(character:dict, class_data: dict) -> dict:
    character_class_name = character["character"]["class"]
    character_level = str(character["character"]["level"])

    pathway = None
    for pathway_data in class_data.values():
        if pathway_data["name"] == character_class_name:
            pathway = pathway_data
            break

    if pathway is None:
        raise ValueError(f"No pathway found for class '{character_class_name}'.")

    level_data = pathway["level"][character_level]
    trait_bonuses = {}

    for trait_key, trait in level_data["traits"].items():
        effect = trait.get("effect", {})

        if effect:
            trait_bonuses[trait_key] = effect

    character["character"]["trait_bonuses"] = trait_bonuses

    return character


def create_character(character: str, player: str, file: str, pathway: str, class_data: dict, items_data: dict) -> dict:
    character_data = open_json(file)

    character_data["character"]["name"] = character
    character_data["character"]["player"] = player
    character_data["character"]["class"] = pathway
    character_data["character"]["level"] = 1
    character_data["character"]["xp"] = 0
    character_data["character"]["trait_bonuses"] = {}

    character_data = apply_class_traits(character_data, class_data)

    effective = get_effective_stats(character_data, items_data)
    hp_multiplier = character_data["character"]["derived_stats"]["max_health"]["multiplier"]
    mana_multiplier = character_data["character"]["derived_stats"]["max_mana"]["multiplier"]
    character_data["character"]["current"]["health"] = effective["constitution"] * hp_multiplier
    character_data["character"]["current"]["mana"] = effective["intellect"] * mana_multiplier

    print(f"Welcome, {character}!")
    print(f"Class: {pathway} (level 1)")
    print(f"HP: {character_data['character']['current']['health']} | "
          f"Mana: {character_data['character']['current']['mana']}")

    return character_data


def is_alive(character: dict) -> bool:
    try:
        if character["character"]["current"]["health"] > 0:
            return True
    except KeyError:
        raise ValueError("One or more keys for current health don't exist.")
    else:
        return False


def equip_item(character: dict, item_name: str, items_data: dict) -> dict:
    items_by_name = {item["name"]: item for item in items_data["items"]}

    if item_name not in items_by_name:
        raise ValueError(f"Item '{item_name}' not found in items data.")

    item = items_by_name[item_name]

    if item["type"] != "equipment":
        raise ValueError(f"Item '{item_name}' is not an equippable item.")

    slot = item["slot"]
    inventory = character["character"]["inventory"]
    inventory_names = [index["name"] for index in inventory]

    if item_name not in inventory_names:
        raise ValueError(f"'{item_name}' is not in {character['character']['name']}'s inventory.")

    current_equipped = character["character"]["equipment"][slot]
    if current_equipped:
        character = unequip_item(character, slot, items_data)

    character["character"]["equipment"][slot] = item_name
    inventory_item = next(item for item in inventory if item["name"] == item_name)
    inventory.remove(inventory_item)

    print(f"You equipped {item_name}.")
    return character


def unequip_item(character: dict, slot: str, items_data: dict) -> dict:
    item_name = character["character"]["equipment"].get(slot)

    if not item_name:
        print(f"Nothing equipped in {slot}.")
        return character

    items_by_name = {item["name"]: item for item in items_data["items"]}
    item_data = items_by_name[item_name]

    character["character"]["inventory"].append({
        "name": item_name,
        "type": "equipment",
        "slot": slot,
        "stats": item_data["stats"]
    })
    character["character"]["equipment"][slot] = None

    print(f"You unequipped {item_name}.")
    return character


def award_xp(character: dict, amount: int, class_data: dict, items_data: dict) -> dict:
    xp_thresholds = {2: 100, 3: 300}

    character["character"]["xp"] += amount
    print(f"You gained {amount} xp! | Total: {character['character']['xp']} xp")

    current_level = character["character"]["level"]
    next_level = current_level + 1

    if next_level in xp_thresholds and character["character"]["xp"] >= xp_thresholds[next_level]:
        character = level_up(character, class_data, items_data)

    return character


def level_up(character: dict, class_data: dict, items_data: dict) -> dict:
    old_level = character["character"]["level"]
    new_level = old_level + 1
    character["character"]["level"] = new_level

    pathway_name = character["character"]["class"]
    pathway = next(pathway for pathway in class_data.values() if pathway["name"] == pathway_name)
    new_class_name = pathway["level"][str(new_level)]["name"]

    print("*** Level Up! ***")
    print(f"You are now level {new_level}: {new_class_name}!")

    character = apply_class_traits(character, class_data)

    effective = get_effective_stats(character, items_data)
    hp_multiplier = character["character"]["derived_stats"]["max_health"]["multiplier"]
    mana_multiplier = character["character"]["derived_stats"]["max_mana"]["multiplier"]
    new_max_hp = effective["constitution"] * hp_multiplier
    new_max_mana = effective["intellect"] * mana_multiplier

    character["character"]["current"]["health"] = new_max_hp
    character["character"]["current"]["mana"] = new_max_mana

    print(f"Max HP: {new_max_hp} | Max Mana: {new_max_mana}")
    print(f"Your hp and mana have been fully restored!")

    return character


def main():
    pass


if __name__ == '__main__':
    main()