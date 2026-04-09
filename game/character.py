import json
from file_tampering import open_json

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
                file_object.seek(0)
                json.dump(character_data, file_object, indent=4)
    return


def is_alive(file: str) -> bool:
    character_data = open_json(file)

    try:
        if character_data["character"]["current"]["health"] > 0:
            return True
    except KeyError:
        raise ValueError("One or more keys for current health don't exist.")
    else:
        return False


def character_class(file: str):
    class_data = open_json(file)

    while True:
        pick_class = str(input("What is your character's pathway? ")).strip().title()
        if len(pick_class) > 0:
            if pick_class in class_data["pathway"]["name"]:
                validate = str(
                    input(f"Your character will be a knight of the {class_data["pathway"]["name"]} pathway. Are you "
                          f"sure about that? (y/n) ")).strip().lower()
                if validate == 'y':
                    break
                elif validate == 'n':
                    continue
                else:
                    print("Please input 'y' or 'n'.")
                    continue
        else:
            print("Your character's pathway can't be empty.")
            continue
    return pick_class


def equip_item():
    pass


def validate_equip():
    pass


def see_inventory():
    pass


def level_up():
    pass


def main():
    pass


if __name__ == '__main__':
    main()