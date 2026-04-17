import character, file_tampering, map, combat


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
    events_by_id = {event["id"]: event for event in events["events"]}
    class_data = file_tampering.open_json("../json_files/classes.json")
    items_data = file_tampering.open_json("../json_files/items.json")

    character_file = "../json_files/character.json"
    character_name = character.character_name()
    player_name = character.player_name()
    class_name = character.character_class("../json_files/classes.json")

    character_data = character.create_character(character_name, player_name, character_file, class_name,
                                                class_data, items_data)


    map.display_map(character_data, atlas, events_by_id)
    map.describe_location(events_by_id, character_data, atlas)

    while character.is_alive(character_data):
        direction = map.get_user_choice()
        valid_move = map.validate_move(direction, character_data, atlas)

        if valid_move:
            map.move_character(character_data, direction)
            map.display_map(character_data, atlas, events_by_id)
            map.describe_location(events_by_id, character_data, atlas)

            character_x = character_data["character"]["location"]["character_x"]
            character_y = character_data["character"]["location"]["character_y"]
            character_z = character_data["character"]["location"]["character_z"]
            event_id = atlas[character_z]["position"][(character_y, character_x)]

            if events_by_id[event_id]["type"] == "fight":
                combat.combat(character_data, events_by_id, atlas, class_data, items_data)
                map.display_map(character_data, atlas, events_by_id)
        else:
            map.display_map(character_data, atlas, events_by_id)
            print("You can't go that way. Try again")
    return


def main():
    """
    Drive the program.
    """
    game()


if __name__ == '__main__':
    main()