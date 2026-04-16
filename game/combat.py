import random



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

    print("Inventory:")
    for index, item in enumerate(consumables, 1):
        print(f"{index}: {item['name']}")

    return


def use_item(character):
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





def apply_item_effect(character, items):
    pass


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
    return


if __name__ == '__main__':
    main()