import random
from game.colours import Colours, colourize


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
    """
    display = []

    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]
    character_z = character["character"]["location"]["character_z"]

    # Print current location info
    print(colourize(f"\n📍 Current Position: Floor {character_z + 1}, ({character_x}, {character_y})", Colours.CYAN))

    current_layer = character_z

    # Get grid dimensions
    positions = list(atlas[current_layer]["position"].keys())
    if not positions:
        return

    max_row = max(pos[0] for pos in positions)
    max_col = max(pos[1] for pos in positions)

    # Print column numbers
    print("   ", end="")
    for col in range(max_col + 1):
        print(f" {col} ", end="")
    print()

    # Create a grid
    for row in range(max_row + 1):
        print(f"{row:2} ", end="")
        for col in range(max_col + 1):
            position = (row, col)
            if position not in atlas[current_layer]["position"]:
                print("   ", end="")
                continue

            value = atlas[current_layer]["position"].get(position)

            if (character_y, character_x) == position:
                print(colourize(" @ ", Colours.SPECIAL), end="")
            elif value is None:
                print(colourize(" . ", Colours.WARNING), end="")
            elif value == 11:
                print(colourize(" S ", Colours.CYAN), end="")
            else:
                event = events.get(value, {})
                event_type = event.get("type", "unknown")

                if event_type == "chest":
                    print(colourize(" C ", Colours.BUFF), end="")
                elif event_type == "fight":
                    print(colourize(" F ", Colours.FAIL), end="")
                elif event_type == "boon":
                    print(colourize(" B ", Colours.HEAL), end="")
                elif event_type == "debuff":
                    print(colourize(" D ", Colours.DEBUFF), end="")
                elif event_type == "boss":
                    print(colourize(" ⚔️ ", Colours.TITLE), end="")
                else:
                    print(colourize(" ? ", Colours.WARNING), end="")
        print()

    # Print legend
    print(colourize("\nLegend:", Colours.CYAN))
    print(
        f"{colourize('@', Colours.SPECIAL)} = You     {colourize('C', Colours.BUFF)} = Chest     {colourize('B', Colours.HEAL)} = Boon")
    print(
        f"{colourize('F', Colours.FAIL)} = Fight   {colourize('D', Colours.DEBUFF)} = Debuff   {colourize('S', Colours.CYAN)} = Stairs")
    print(f"{colourize('⚔️', Colours.TITLE)} = Boss    {colourize('.', Colours.WARNING)} = Empty")

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
            print("\nYou are standing on empty ground.")
        elif event_id == 11:
            print("\nStairs leading to the next floor are here.")
        else:
            return print(f"{events[event_id]['description']}")


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
        print("\n1: North, 2: East, 3: South, 4: West")
        try:
            direction = int(input("Enter the direction you wish to travel: "))
        except ValueError:
            print("\nPlease enter a valid integer.")
        else:
            if direction in compass:
                break
            else:
                print("\nPlease enter a number corresponding to one of the directions.")
                continue
    return direction


def move_character(character: dict, direction: int) -> dict:
    """
    Move a character in one of four cardinal directions by updating their coordinates.

    Direction mapping:
    - 1: North (decrease y)
    - 2: East (increase x)
    - 3: South (increase y)
    - 4: West (decrease x)
    """
    if direction == 1:  # North
        character["character"]["location"]["character_y"] -= 1
        print(
            f"\nYou move North to ({character['character']['location']['character_x']}, {character['character']['location']['character_y']})")
    elif direction == 2:  # East
        character["character"]["location"]["character_x"] += 1
        print(
            f"\nYou move East to ({character['character']['location']['character_x']}, {character['character']['location']['character_y']})")
    elif direction == 3:  # South
        character["character"]["location"]["character_y"] += 1
        print(
            f"\nYou move South to ({character['character']['location']['character_x']}, {character['character']['location']['character_y']})")
    else:  # West
        character["character"]["location"]["character_x"] -= 1
        print(
            f"\nYou move West to ({character['character']['location']['character_x']}, {character['character']['location']['character_y']})")
    return character


def validate_move(direction: int, character: dict, atlas: dict) -> bool:
    """
    Validate whether a character can move to a target position on the atlas map.

    Direction mapping:
    - 1: North (y - 1)
    - 2: East (x + 1)
    - 3: South (y + 1)
    - 4: West (x - 1)
    """
    character_z = character["character"]["location"]["character_z"]
    character_x = character["character"]["location"]["character_x"]
    character_y = character["character"]["location"]["character_y"]

    # Calculate target coordinates
    if direction == 1:  # North
        target_y = character_y - 1
        target_x = character_x
    elif direction == 2:  # East
        target_y = character_y
        target_x = character_x + 1
    elif direction == 3:  # South
        target_y = character_y + 1
        target_x = character_x
    elif direction == 4:  # West
        target_y = character_y
        target_x = character_x - 1
    else:
        return False

    target_position = (target_y, target_x)

    if target_position in atlas[character_z]["position"]:
        return True
    else:
        return False


def traverse_stairs(character: dict, direction: str, atlas: dict) -> dict:
    """
    Move a character between floors of the atlas if a valid stair transition exists.

    The function adjusts the character's vertical position (z-axis) based on the
    direction provided. The character can only move within the bounds of the atlas:
    - "down" increases the floor level (goes deeper)
    - "up" decreases the floor level (goes higher)

    If the movement is not possible (invalid direction or out-of-bounds floor),
    a message is printed and no movement occurs.

    :param character: A dictionary containing character data, including location coordinates
    :param direction: A string indicating stair movement ("up" or "down")
    :param atlas: A dictionary representing the multi-layer map structure
    :precondition: character contains "location" with a valid "character_z" value
                   atlas contains at least one valid floor layer
    :postcondition: update the character's floor (z-coordinate) if movement is valid
    :returns: the updated character dictionary
    """
    current_z = character["character"]["location"]["character_z"]

    if direction == "down" and current_z < len(atlas) - 1:
        character["character"]["location"]["character_z"] += 1
        print(f"\nYou descend to floor {character['character']['location']['character_z'] + 1}.")
    elif direction == "up" and current_z > 0:
        character["character"]["location"]["character_z"] -= 1
        print(f"\nYou ascend to floor {character['character']['location']['character_z'] + 1}.")
    else:
        print("You can't go that way.")

    return character


def main():
    return


if __name__ == '__main__':
    main()
