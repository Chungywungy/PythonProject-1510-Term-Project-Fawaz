import random


def build(layers: int, rows: int, columns: int) -> dict:
    """
    Generate a multi-layer atlas map with randomly assigned tile values and guaranteed stair placement.

    The function builds a 3D-like structure represented as nested dictionaries.
    Each layer contains a grid of (row, column) positions mapped to tile IDs.

    Tile values are randomly assigned:
    - Values 1–10 represent normal tiles
    - Value 11 represents a stair tile

    The first tile in layer 0 at position (0, 0) is always set to None.

    Stair rules:
    - Each non-final layer must contain at least one stair tile (value 11)
    - If no stairs are generated, one is forcibly added
    - If multiple stairs exist, extra stairs are removed

    :param layers: Number of layers in the atlas
    :param rows: Number of rows per layer grid
    :param columns: Number of columns per layer grid
    :precondition: layers, rows, and columns are positive integers
    :postcondition: generate a structured atlas dictionary with valid tile placement
    :returns: a dictionary representing the full multi-layer atlas map
    :raises TypeError: if layers, rows, or columns are not integers
    """
    atlas = dict()

    if (type(layers) or type(rows) or type(columns)) != int:
        raise TypeError("layers, rows, and columns must be integers")
    else:
        for layer in range(layers):
            atlas[layer] = {"position": {}}

            for row in range(rows):
                for column in range(columns):
                    if layer == 0 and row == 0 and column == 0:

                        atlas[layer]["position"][(row, column)] = None
                    else:
                        if layer < layers - 1:
                            if random.random() < 0.1 and (row, column) != (0, 0):
                                atlas[layer]["position"][(row, column)] = 11
                            else:
                                atlas[layer]["position"][(row, column)] = random.choice(range(1, 11))
                        else:
                            atlas[layer]["position"][(row, column)] = random.choice(range(1, 11))

    for layer in range(layers - 1):
        stair_count = sum(1 for pos_id in atlas[layer]["position"].values() if pos_id == 11)

        if stair_count == 0:
            positions = [(row, col) for row in range(rows) for col in range(columns)
                         if (layer != 0 or (row, col) != (0, 0))]
            random_pos = random.choice(positions)
            atlas[layer]["position"][random_pos] = 11
        elif stair_count > 1:
            stair_positions = [pos for pos, pos_id in atlas[layer]["position"].items() if pos_id == 11]
            for pos in stair_positions[1:]:
                atlas[layer]["position"][pos] = random.choice(range(1, 11))

    return atlas


def display_map(character: dict, atlas: dict, events: dict) -> None:
    """
    Display the current layer of the atlas map with the character and event markers.

    The function renders a visual representation of the current map layer based on
    the character's position. Different symbols are used to represent tiles:

    - "@" represents the player's current position
    - "-" represents empty or normal tiles
    - "C" represents chest events
    - "S" represents stair tiles


    :param character: A dictionary containing character data, including location coordinates
    :param atlas: A dictionary representing the multi-layer map structure
    :param events: A dictionary mapping tile IDs to event data
    :precondition: character contains valid "location" with x, y, z coordinates
                  atlas contains a valid layer structure with "position" data
                  events contains valid event mappings for tile IDs
    :postcondition: print current map layer to the console
    :returns: None
    """
    display = []

    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    current_layer = character_z

    for position in atlas[current_layer]["position"]:
        value = atlas[current_layer]["position"].get(position)

        if (character_y, character_x) == position:
            display.append("@")
        elif value is None:
            display.append("-")
        elif events[value].get("type") == "chest":
            display.append("C")
        elif value == 11:
            display.append("S")
        else:
            display.append("-")

    for index, point in enumerate(display):
        print(point, end=" ")
        if (index + 1) % 5 == 0:
            print()
    return


def describe_location(events: dict, character: dict, atlas: dict) -> None:
    """
    Describe the player's current location based on the atlas tile and event data.

    The function checks the character's current coordinates and retrieves the tile
    value from the atlas. It then prints a description depending on the tile type:

    - None → empty ground
    - 11 → stairs to next floor
    - otherwise → event description from events dictionary

    If the character has no valid location data, a KeyError is raised.

    :param events: Dictionary of event data indexed by tile ID
    :param character: Character dictionary containing location coordinates
    :param atlas: Multi-layer map structure containing tile positions
    :precondition: character contains valid "location" with x, y, z coordinates
                   atlas contains valid positions for the given coordinates
                   events contains valid descriptions for event IDs
    :postcondition: print a description of the current location
    :returns: None

    >>> events = {1: {"description": "A dusty old chest."}}
    >>> atlas = {0: {"position": {(0, 0): 1}}}
    >>> character = {"character": {"location": {"character_x": 0, "character_y": 0, "character_z": 0}}}
    >>> describe_location(events, character, atlas)
    A dusty old chest.

    >>> atlas = {0: {"position": {(0, 0): None}}}
    >>> describe_location({}, character, atlas)
    You are standing on empty ground.

    >>> atlas = {0: {"position": {(0, 0): 11}}}
    >>> describe_location({}, character, atlas)
    Stairs leading to the next floor are here.
    """
    try:
        character_x = character["character"]["location"]["character_x"]
        character_y = character["character"]["location"]["character_y"]
        character_z = character["character"]["location"]["character_z"]
    except KeyError:
        raise KeyError("The character does not have a location.")
    else:
        event_id = atlas[character_z]["position"][(character_y, character_x)]
        if event_id is None:
            print("You are standing on empty ground.")
        elif event_id == 11:
            print("Stairs leading to the next floor are here.")
        else:
            return print(events[event_id]["description"])


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
    """
    Move a character in one of four cardinal directions by updating their coordinates.

    The function updates the character's location in-place based on the given
    direction value:
    - 1: North (decrease y)
    - 2: East (increase x)
    - 3: South (increase y)
    - 4: West (decrease x)

    :param character: A dictionary containing character data, including location coordinates
    :param direction: An integer representing movement direction (1–4)
    :precondition: character contains a valid "location" dictionary with "character_x" and "character_y"
                   direction is expected to be an integer between 1 and 4
    :postcondition: update the character's x or y coordinate based on direction
    :returns: the updated character dictionary
    """
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
    """
    Validate whether a character can move to a target position on the atlas map.

    The function calculates the target coordinates based on the given direction
    and checks whether the destination tile exists in the current layer of the atlas.
    A move is considered valid only if the target position exists and contains a
    truthy value in the atlas.

    Direction mapping:
    - 1: North (y - 1)
    - 2: East (x + 1)
    - 3: South (y + 1)
    - 4: West (x - 1)

    :param direction: An integer representing movement direction (1–4)
    :param character: A dictionary containing character location data
    :param atlas: A dictionary representing the multi-layer map structure
    :precondition: character contains "location" with x, y, z coordinates
                   atlas contains a valid "position" dictionary for the current layer
    :postcondition: validate character movement
    :returns: True if the move is valid, otherwise False
    """
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


def traverse_stairs(character: dict, direction: str, atlas: dict) -> dict:
    current_z = character["character"]["location"]["character_z"]

    if direction == "down" and current_z < len(atlas) - 1:
        character["character"]["location"]["character_z"] += 1
        print(f"You descend to floor {character['character']['location']['character_z'] + 1}.")
    elif direction == "up" and current_z > 0:
        character["character"]["location"]["character_z"] -= 1
        print(f"You ascend to floor {character['character']['location']['character_z'] + 1}.")
    else:
        print("You can't go that way.")

    return character



def main():
    return


if __name__ == '__main__':
    main()