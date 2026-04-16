import json
from file_tampering import open_json
from combat import combat

def character_name() -> str:
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


def create_character(character: str, player: str, file: str, pathway: str):
    if ".json" not in file:
        raise ValueError("File is not a JSON file.")
    else:
        with open(file, 'r+') as file_object:
            try:
                character_data = json.load(file_object)
            except json.JSONDecodeError:
                raise ValueError("The JSON file is empty.")
            else:
                character_data["character"]["name"] = character
                character_data["character"]["player"] = player
                character_data["character"]["class"] = pathway
    return character_data


def is_alive(character: dict) -> bool:
    try:
        if character["character"]["current"]["health"] > 0:
            return True
    except KeyError:
        raise ValueError("One or more keys for current health don't exist.")
    else:
        return False



def commands(character):
    def equip():
        pass

    def inventory():
        pass

    def use_item():
        pass


    pass


def validate_equip():
    pass


def level_up():
    pass


def main():
    pass


if __name__ == '__main__':
    main()