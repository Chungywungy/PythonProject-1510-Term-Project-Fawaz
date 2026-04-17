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
    mc_name = str(input("\x1b[1;35m What is your characters' name? ").strip().title())

    while True:
        if len(mc_name) == 0:
            validate = str(input("\nThe default name is Amon. Are you sure about your choice? (y/n) ")).strip().lower()
            if validate == 'y':
                mc_name = 'Amon'
                break
            elif validate == 'n':
                mc_name = str(input("\nWhat is your characters' name? ").strip().title())
                continue
            else:
                print("\nPlease input 'y' or 'n'.")
                continue
        else:
            validate = str(
                input(f"\nYour character's name is {mc_name}. Are you sure about that? (y/n) ")).strip().lower()
            if validate == 'y':
                break
            elif validate == 'n':
                mc_name = str(input("\nWhat is your characters' name? ").strip().title())
                continue
            else:
                print("\nPlease input 'y' or 'n'.")
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
    player = str(input("\nWhat is your name oh mighty player? ")).strip().title()

    while True:
        if len(player) == 0:
            player = str(input("\nYou can't have no name. Now tell me what is your name? ")).strip().title()
            continue
        else:
            validate = str(
                input(f"\nYour name is {player}. Are you sure about that? (y/n) ")).strip().lower()
            if validate == 'y':
                break
            elif validate == 'n':
                player = str(input("\nWhat is your name, player? ").strip().title())
                continue
            else:
                print("\nPlease input 'y' or 'n'.")
                continue
    return player


def character_class(file: str):
    """
    Prompt the user to select and confirm a character pathway from a JSON file.

    The function loads pathway data from a JSON file, displays the available
    pathway names, and prompts the user to choose one. The user must enter a
    valid, non-empty pathway name and confirm their selection. The process
    repeats until a valid and confirmed pathway is chosen.

    :param file: the path to the JSON file containing pathway data as a string
    :precondition: file is a valid path to a JSON file with properly formatted pathway data
    :postcondition: valid character pathway name is returned as a string
    :returns: the confirmed character pathway name as a string
    """
    class_data = open_json(file)

    pathway_names = {data["name"]: key for key, data in class_data.items()}

    while True:
        print("\nAvailable pathways:")

        for key, data in class_data.items():
            print(f"\n{data['name']}: {data['description']}")

        pick_class = str(input("\nWhat is your character's pathway? ")).strip().title()

        if len(pick_class) == 0:
            print("\nyour character's pathway can't be empty.")
            continue
        if pick_class not in pathway_names:
            print(f"\n{pick_class} is not a valid pathway. Please choose from the list of available pathways.")
            continue

        validate = str(input(f"\nyour character will follow the {pick_class} pathway.\n"
                             f"Are you sure about that? (y/n) ")).strip().lower()

        if validate == 'y':
            break
        elif validate == 'n':
            continue
        else:
            print("Please input 'y' or 'n'.")

    return pick_class


def get_effective_stats(character: dict, items_data: dict) -> dict:
    """
    Calculate and return a character's effective stats based on base stats,
    trait bonuses, and equipped items.

    The function starts with the character's base stats, then applies any
    bonuses from traits, followed by stat increases from equipped items.
    Only valid stats present in the base stats are modified.

    :param character: A dictionary containing character data, including base stats,
                     trait bonuses, and equipped items
    :param items_data: A dictionary containing item data, including equipment stats
    :precondition: character contains "character", "base_stats", and "equipment" keys
                  items_data contains an "items" list with valid equipment entries
    :postcondition: create a dictionary of effective stats with all applicable bonuses applied
    :returns: a dictionary representing the character's effective stats
    """
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


def apply_class_traits(character: dict, class_data: dict) -> dict:
    """
    Apply class trait bonuses to a character based on their class and level.

    The function searches the class data for the character's current class,
    retrieves the appropriate level data, and extracts trait effects. These
    effects are stored as trait bonuses inside the character dictionary.

    If the character's class cannot be found in the class data, a ValueError
    is raised.

    :param character: A dictionary containing character data, including class and level
    :param class_data: A dictionary containing all available class/pathway definitions
    :precondition: character contains "character", "class", and "level" keys
                   class_data contains valid pathway entries with level data
    :postcondition: update character dictionary with a "trait_bonuses" key
    :returns: the updated character dictionary with applied trait bonuses
    :raises ValueError: if the character's class is not found in class_data
    """
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
    """
    Create and initialize a new character with base stats, class traits, and derived attributes.

    The function loads a character template from a JSON file, assigns basic identity
    fields (name, player, class, level), and initializes experience and trait bonuses.
    It then applies class traits and calculates effective stats using class and item data.

    Finally, derived stats such as health and mana are calculated using multipliers
    from the character's configuration and printed as a welcome summary.

    :param character: The name of the character being created
    :param player: The name of the player controlling the character
    :param file: Path to the JSON file containing the base character template
    :param pathway: The selected class/pathway name
    :param class_data: Dictionary containing class definitions and traits
    :param items_data: Dictionary containing item and equipment data
    :precondition: file is a valid JSON file path with a valid character structure
                  class_data contains valid class definitions
                  items_data contains valid equipment definitions
    :postcondition: A fully initialized character dictionary is created and returned
    :returns: a dictionary representing the fully created character
    """
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

    print(f"\nWelcome, {character}!")
    print(f"Class: {pathway} (level 1)")
    print(f"HP: {character_data['character']['current']['health']} | "
          f"Mana: {character_data['character']['current']['mana']}")

    return character_data


def is_alive(character: dict) -> bool:
    """
    Check whether a character is alive based on their current health.

    The function checks the character's current health value. If health is
    greater than 0, the character is considered alive. If required keys are
    missing, a ValueError is raised.

    :param character: A dictionary containing character data with current health
    :precondition: character contains "character" -> "current" -> "health" keys
    :postcondition: calculate True if health > 0, otherwise False
    :returns: True if the character is alive, False if dead
    :raises ValueError: if required keys are missing
    """
    try:
        if character["character"]["current"]["health"] > 0:
            return True
    except KeyError:
        raise ValueError("One or more keys for current health don't exist.")
    else:
        return False


def equip_item(character: dict, item_name: str, items_data: dict) -> dict:
    """
    Equip an item to a character from their inventory and update their equipment slots.

    The function validates that the item exists in the items data, is of type "equipment",
    and is present in the character's inventory. If another item is already equipped in
    the same slot, it is first unequipped. The item is then moved from inventory to the
    appropriate equipment slot.

    If the item does not exist, is not equippable, or is not in the character's inventory,
    a ValueError is raised.

    :param character: A dictionary containing character data, including inventory and equipment
    :param item_name: The name of the item to equip
    :param items_data: A dictionary containing item definitions and data
    :precondition: character contains "inventory" and "equipment" keys
                   items_data contains valid item definitions with "name", "type", and "slot"
    :postcondition: update character's equipment and inventory accordingly
    :returns: the updated character dictionary with the item equipped
    :raises ValueError: if the item is not found, not equippable, or not in inventory
    """
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
    """
    Unequip an item from a character's equipment slot and return it to the inventory.

    The function checks the specified equipment slot. If an item is equipped,
    it retrieves the item data from items_data, adds the item back into the
    character's inventory, and clears the equipment slot. If no item is
    equipped in the slot, the function prints a message and returns the
    character unchanged.

    :param character: A dictionary containing character data, including inventory and equipment
    :param slot: The equipment slot to unequip from (e.g., "weapon", "armor")
    :param items_data: A dictionary containing item definitions and stats
    :precondition: character contains valid "inventory" and "equipment" structures
                   items_data contains matching item definitions for equipped items
    :postcondition: remove item (if any) from equipment and add to inventory
    :returns: the updated character dictionary
    """
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


def level_up(character: dict, class_data: dict, items_data: dict) -> dict:
    """
    Increase a character's level and update their class traits and derived stats.

    The function increments the character's level, determines the new class name
    based on the pathway data, and prints level-up messages. It then reapplies
    class traits, recalculates effective stats, and updates the character's
    maximum health and mana based on derived stat multipliers.

    Health and mana are fully restored after leveling up.

    :param character: A dictionary containing character data, including level, class, and stats
    :param class_data: A dictionary containing class/pathway definitions and level progression
    :param items_data: A dictionary containing item definitions used for stat calculation
    :precondition: character contains valid level, class, derived_stats, and current stats
                  class_data contains valid pathway and level definitions
                  items_data contains valid item structures
    :postcondition: update the character's level, traits, and derived stats
    :returns: the updated character dictionary after leveling up
    """
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
