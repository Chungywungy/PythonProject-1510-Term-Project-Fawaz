import random


def build(layers, rows, columns):
    atlas = dict()

    if (type(layers) or type(rows) or type(columns)) != int:
        raise TypeError("layers, rows, and columns must be integers")
    else:
        for layer in range(layers + 1):
            atlas[layer] = {"position": {}}
            for row in range(rows + 1):
                for column in range(columns + 1):
                    atlas[layer]["position"][(row, column)] = random.choice(range(1, 11))

    return atlas


def display_map(character: dict, atlas: dict) -> None:
    display = []

    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    current_layer = character_z

    for position in atlas[current_layer]["position"]:
        value = atlas[current_layer]["position"].get(position)

        if (character_x, character_y) == position:
            display.append("@")
        elif value == 1 or value == 2:
            display.append("C")
        else:
            display.append("-")

    for index, point in enumerate(display):
        print(point, end=" ")
        if (index + 1) % 5 == 0:
            print()
    return


def describe_location(events: dict, character: dict, atlas: dict) -> str:
    try:
        character_x = character["character"]["location"]["character_x"]
        character_y = character["character"]["location"]["character_y"]
        character_z = character["character"]["location"]["character_z"]
    except KeyError:
        raise KeyError("The character does not have a location.")
    else:
        return events["events"][atlas[character_z]["position"][(character_x, character_y)]]["description"]


def get_user_choice() -> int:
    """
    Get the direction.

    A simple function that takes user input and converts it into one of the four
    cardinal directions.

    :postcondition: Store a valid integer corresponding to a direction
    :return: an integer representing one of the four cardinal directions
    """
    compass = {1, 2, 3, 4}

    while True:
        print("1: North, 2: East, 3: South, 4: West")
        try:
            direction = int(input("Enter the direction you wish to travel: "))
        except ValueError:
            print("Please enter a valid integer.")
        else:
            if direction in compass:
                break
            else:
                print("Please enter a number corresponding to one of the directions.")
                continue
    return direction



def move_character(character: dict, direction: int) -> dict:
    if direction == 1:
        character["character"]["location"]["character_y"] -= 1
    elif direction == 2:
        character["character"]["location"]["character_x"] += 1
    elif direction == 3:
        character["character"]["location"]["character_y"] += 1
    else:
        character["character"]["location"]["character_x"] -= 1
    return character


def validate_move(direction: int, character: dict, atlas: dict) -> bool:
    character_z = character["character"]["location"]["character_z"]

    if direction == 1:
        character_x = character["character"]["location"]["character_x"]
        character_y = character["character"]["location"]["character_y"] - 1
    elif direction == 2:
        character_x = character["character"]["location"]["character_x"] + 1
        character_y = character["character"]["location"]["character_y"]
    elif direction == 3:
        character_x = character["character"]["location"]["character_x"]
        character_y = character["character"]["location"]["character_y"] + 1
    elif direction == 4:
        character_x = character["character"]["location"]["character_x"] - 1
        character_y = character["character"]["location"]["character_y"]
    else:
        return False

    if atlas[character_z]["position"].get((character_x, character_y)):
        return True
    else:
        return False



def main():
    return


if __name__ == '__main__':
    main()