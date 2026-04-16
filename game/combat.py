import random
import character


def get_combat_command() -> int:
    options = {1: "Attack", 2: "Items", 3: "Flee"}

    while True:
        print("What will you do?")
        for key, value in options.items():
            print(f"{key}: {value}")
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter an integer!")
        else:
            if choice in options:
                return choice
            else:
                print("Please enter a number corresponding to one of the options.")


def player_attack(character, events):
    pass


def display_inventory(character: dict) -> None:
    inventory = character["character"]["inventory"]
    consumables = [item for item in inventory if item["type"] == "consumable"]

    if len(consumables) == 0:
        print(f"{character['character']['name']} has no consumable items!")
        return

    print("Inventory:")
    for index, item in enumerate(consumables, 1):
        print(f"{index}: {item['name']}")

    return


def flee(character: dict) -> bool:
    chance = random.random()

    if chance >= 0.5:
        print(f"{character['character']['name']} successfully fled from combat!")
        return True
    else:
        print("You failed to flee!")
        return False


def enemy_behaviour(events, atlas, character):
    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    location = atlas[character_z]["position"][(character_y, character_x)]

    attacks = events["events"][location]["enemy"]["attacks"]

    chosen_attack = random.choice(attacks)

    description = chosen_attack["description"]
    damage = chosen_attack["damage"]

    character["character"]["current"]["health"] -= damage
    print(f"{description}\nYou take {damage} damage!\n"
          f"You have {character["character"]["current"]["health"]} HP remaining.")
    return


def boss_behaviour():
    pass


def combat():
    pass


def main():
    return display_inventory(character.create_character("Bob","Fawaz", "../json_files/character.json", "Sun"))


if __name__ == '__main__':
    main()