import character, file_tampering, map



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
    layers = 2

    atlas = map.build(layers, rows, columns)
    events = file_tampering.open_json("../json_files/events.json")

    character_file = "../json_files/character.json"
    class_name = character.character_class("../json_files/classes.json")
    character_name = character.character_name()
    player_name = character.player_name()

    character_data = character.create_character(character_name, player_name, character_file, class_name)

    map.display_map(character_data, atlas, events)
    map.describe_location(events, character_data, atlas)
    while character.is_alive(character_data):
        direction = map.get_user_choice()
        valid_move = map.validate_move(direction, character_data, atlas)
        if valid_move:
            map.move_character(character_data, direction)
            map.display_map(character_data, atlas, events)
            map.describe_location(events, character_data, atlas)
        else:
            map.display_map(character_data, atlas, events)
            print("You can't go that way. Try again")
    return


def main():
    """
    Drive the program.
    """
    game()


if __name__ == '__main__':
    main()