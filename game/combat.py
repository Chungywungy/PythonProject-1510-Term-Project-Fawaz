import random


def combat():
    pass


def enemy_behaviour(events, atlas, character):
    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    location = atlas[character_z]["position"][(character_x, character_y)]

    attacks = events["events"][location]["enemy"]["attacks"]

    chosen_attack = random.choice(attacks)

    description = chosen_attack["description"]
    damage = chosen_attack["damage"]

    print(f"{description}\nYou take {damage} damage!")
    return


def boss_behaviour():
    pass


def main():
    pass


if __name__ == '__main__':
    main()