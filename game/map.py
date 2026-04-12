import random


def build_map(layers, rows, columns):
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


def display_map():
    pass


def describe_location(events: str, character: str, atlas: dict) -> str:
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


def character_direction():
    pass


def move_character():
    pass


def validate_move():
    pass


def main():
    pass


if __name__ == '__main__':
    main()