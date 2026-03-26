from random import randint


def make_board(rows: int, columns: int) -> dict[tuple[int, int], str]:
    """
    Create a 2d board.

    A simple function that creates a dictionary with coordinates for a board with a certain
    amount of rows and columns.

    :param rows: a non-zero positive integer
    :param columns: a non-zero positive integer
    :precondition: rows and columns must both be positive integers greater than 0
    :postcondition: Create a dictionary with the keys as a tuple(rows, columns) and the values
                    as a random string description
    :return: a dictionary with the keys as a tuple with integer coordinates and the values as
             a random string description

    >>> len(make_board(1, 1))
    1
    >>> len(make_board(10, 10))
    100
    """
    count_rows = 0
    board = dict()
    room_description = ["Empty room", "Lava room", "Water room"]

    if (type(rows) or type(columns)) is not int or ((rows <= 0) or (columns <= 0)):
        raise ValueError("Please type in an integer greater than 0.")
    else:
        while columns >= 1:
            if count_rows <= (rows - 1):
                board[(count_rows, abs((rows - columns)))] = room_description[randint(0, 2)]
                count_rows += 1
            else:
                columns -= 1
                count_rows = 0
                continue
    return board


def make_character() -> dict[str, int]:
    """
    Create a character.

    A simple function that creates a dictionary with information about the player's character.

    :return: a dictionary containing: "X-coordinate": (int), "Y-coordinate": (int), and "Current HP": (int)

    >>> make_character()
    {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5}
    """
    player = {'X-coordinate': 0,
              'Y-coordinate': 0,
              'Current HP': 5}
    return player


def describe_current_location(board: dict[tuple[int, int], str], character: dict[str, int]) -> str | None:
    """
    Describe the player's current location.

    A simple function that reads the character dictionary and describes the location based on the
    player's X, Y coordinates on the board.

    :param character: a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :param board: a dictionary with the keys as a tuple(rows, columns) and the values
                  as a random string description
    :precondition: board must be a dictionary with the keys as a tuple(rows, columns) and the values
                   as a random string description
    :precondition: character must be a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :postcondition: Get the string value belonging to the key
    :return: a string describing the current location

    >>> board_test = {(0, 0): "Empty room", (1, 0): "Lava room"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> describe_current_location(board_test, character_test)
    Empty room

    >>> character_test = {"X-coordinate": 1, "Y-coordinate": 0}
    >>> describe_current_location(board_test, character_test)
    Lava room
    """
    try:
        x_coordinate = character["X-coordinate"]
        y_coordinate = character["Y-coordinate"]
    except KeyError:
        print(f"Please input coordinates within the range of the board.")
    else:
        return print(board.get((x_coordinate, y_coordinate)))


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


def validate_move(board: dict[tuple[int, int], str], direction: int, character: dict[str, int]) -> bool:
    """
    Check if the player's move is valid.

    :param board: a dictionary with the keys as a tuple(rows, columns) and the values
                  as a random string description
    :param direction: an integer in the range [1, 4]
    :param character: a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :precondition: board must be a dictionary with the keys as a tuple(rows, columns) and the values
                   as a random string description
    :precondition: direction must be an integer in the range [1, 4]
    :precondition: character must be a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :postcondition: Determine if the move is valid(True) or not(False)
    :return: True if the move is valid and False if it's not

    >>> board_test = {(0, 0): "room", (1, 0): "room"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> validate_move(board_test, 2, character_test)
    True

    >>> board_test = {(0, 0): "room"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> validate_move(board_test, 4, character_test)
    False
    """
    if direction == 1:
        character_x = character["X-coordinate"]
        character_y = character["Y-coordinate"] - 1
    elif direction == 2:
        character_x = character["X-coordinate"] + 1
        character_y = character["Y-coordinate"]
    elif direction == 3:
        character_x = character["X-coordinate"]
        character_y = character["Y-coordinate"] + 1
    else:
        character_x = character["X-coordinate"] - 1
        character_y = character["Y-coordinate"]

    if (character_x, character_y) in board:
        return True
    else:
        return False


def move_character(character: dict[str, int], direction: int) -> dict[str, int]:
    """
    Move the player's character in a direction.

    :param character: a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :param direction: an integer in the range [1, 4]
    :precondition: direction must be an integer in the range [1, 4]
    :precondition: character must be a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :postcondition: Calculate the new coordinates of the character
    :return: the player's character's new coordinates

    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> move_character(character_test, 2)
    {'X-coordinate': 1, 'Y-coordinate': 0}
    >>> character_test = {"X-coordinate": 4, "Y-coordinate": 3}
    >>> move_character(character_test, 3)
    {'X-coordinate': 4, 'Y-coordinate': 4}
    """
    if direction == 1:
        character["Y-coordinate"] -= 1
    elif direction == 2:
        character["X-coordinate"] += 1
    elif direction == 3:
        character["Y-coordinate"] += 1
    else:
        character["X-coordinate"] -= 1
    return character


def check_for_foes() -> bool:
    """
    Check for foes.

    A simple function that calculates the odds of a foe showing up.

    :param: None
    :precondition: 'foe' is equal to 1 and 'chance' is a random number between [1, 4]
    :postcondition: calculate equivalence between foe and chance
    :return: True or False
    >>> type(check_for_foes())
    <class 'bool'>
    """
    chance = randint(1, 4)

    if chance == 1:
        return True
    else:
        return False


def guessing_game(character: dict[str, int]) -> None:
    """
    Play a guessing game.

    A function that has the user play a guessing game. The player has to guess an integer between [1, 5]. If they
    guess wrong they lose a single point of HP. If they guess right they win the guessing game and their current hp
    is displayed.

    :param character: a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :precondition: character must be a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :postcondition: Update Character HP and display if the foe has been beaten or not
    """
    foe_attack = randint(1, 5)
    while True:
        try:
            character_attack = int(input("Guess a number between 1 and 5: "))
        except ValueError:
            print("Please input an integer between 1 and 5. ")
        else:
            if character_attack in range(1, 6):
                while foe_attack != character_attack:
                    if character_attack < foe_attack:
                        try:
                            character_attack = int(input("Too low, guess again: "))
                        except ValueError:
                            print("Please input a valid integer between 1 and 5. ")
                        else:
                            character['Current HP'] -= 1
                    else:
                        try:
                            character_attack = int(input("Too high, guess again: "))
                        except ValueError:
                            print("Please input a valid integer between 1 and 5. ")
                        else:
                            character['Current HP'] -= 1

                if character_attack == foe_attack:
                    print(f"You defeated your foe. Your current hp is {character['Current HP']}.")
                    break
            else:
                continue


def check_if_goal_attained(rows: int, columns: int, character: dict[str, int]) -> bool:
    """
    Check if the player's character has reached the goal.

    :param rows: a non-zero positive integer
    :param columns: a non-zero positive integer
    :param character: a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :precondition: rows and columns must be non-zero positive integers
    :precondition: character must be a dictionary containing: "X-coordinate": (int) and "Y-coordinate": (int)
    :postcondition: Calculate if character position is equal to rows - 1 and columns - 1
    :return: True if the character position is equal to rows - 1 and columns - 1, otherwise False

    >>> character_test =  {"X-coordinate": 0, "Y-coordinate": 0}
    >>> check_if_goal_attained(5, 5, character_test)
    False
    >>> character_test =  {"X-coordinate": 4, "Y-coordinate": 4}
    >>> check_if_goal_attained(5, 5, character_test)
    True
    """
    if character.get('X-coordinate') == (rows - 1) and character.get('Y-coordinate') == (columns - 1):
        return True
    else:
        return False


def is_alive(character: dict[str, int]) -> bool:
    """
    Check if the player's character is alive.

    :param character: a dictionary containing: "Current HP": (int)
    :precondition: character must be a dictionary containing: "Current HP": (int)
    :postcondition: Calculate True if the character's hp is greater than 0, otherwise False
    :return: True if the character's hp is greater than 0, otherwise False

    >>> character_test = {'Current HP': 1}
    >>> is_alive(character_test)
    True
    >>> character_test = {'Current HP': 0}
    >>> is_alive(character_test)
    False
    >>> character_test = {'Current HP': -1}
    >>> is_alive(character_test)
    False
    """
    if character.get('Current HP') > 0:
        return True
    else:
        return False


def game() -> None:
    """
    Run the main game loop.

    Initializes the board and character, then repeatedly:
    - prompts the user for movement
    - validates and updates the character's position
    - checks for random encounters
    - updates character HP through the guessing game

    The game ends when the player reaches the goal or runs out of HP.
    """
    rows = 5
    columns = 5
    board = make_board(rows, columns)
    character = make_character()
    achieved_goal = False

    describe_current_location(board, character)
    while is_alive(character) and not achieved_goal:
        direction = get_user_choice()
        valid_move = validate_move(board, direction, character)
        if valid_move:
            move_character(character, direction)
            describe_current_location(board, character)
            there_is_a_challenger = check_for_foes()
            if there_is_a_challenger:
                guessing_game(character)
            achieved_goal = check_if_goal_attained(rows, columns, character)
        else:
            print("You can't go that way. Try again")
    if achieved_goal:
        print("Congratulations! You made it to the goal.")
    else:
        print("Game over! You ran out of HP.")
    return


def main():
    """
    Drive the program.
    """
    game()


if __name__ == '__main__':
    main()