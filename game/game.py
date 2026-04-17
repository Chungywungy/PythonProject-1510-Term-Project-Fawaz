import random

from playsound3 import playsound

from game import character, file_tampering, map, combat, progression



def game() -> None:
    """
    Run the main game loop for the RPG.

    This function initializes the game world, loads map data, events, class data,
    and item data, and creates a player character. It then enters the main gameplay
    loop where the player can move across a multi-layer map, interact with events,
    engage in combat, descend stairs, and eventually face a boss encounter.

    The loop continues until the player either defeats the final boss, dies, or
    chooses to quit after victory. The function handles movement validation, map
    updates, event triggering, combat resolution, XP rewards, and game state updates.

    :precondition: Required JSON files (events, classes, items, character) must exist
    :precondition: map and combat modules must be properly implemented and imported
    :postcondition: modify game state continuously until termination condition is met
    :returns: None
    """
    sound = playsound("sounds/nube_negra_shiro_sagisu.mp3", block=False)

    rows = 5
    columns = 5
    layers = 3

    atlas = map.build(layers, rows, columns)
    events = file_tampering.open_json("json_files/events.json")
    events_by_id = {event["id"]: event for event in events["events"]}
    class_data = file_tampering.open_json("json_files/classes.json")
    items_data = file_tampering.open_json("json_files/items.json")

    boss_id = 12
    if boss_id not in events_by_id:
        events_by_id[boss_id] = {
            "id": 12,
            "type": "boss",
            "name": "Shadow Lord",
            "description": "The Shadow Lord stands before you, radiating dark energy!",
            "enemy": {
                "name": "Shadow Lord",
                "health": 100,
                "attacks": [
                    {"name": "Dark Bolt", "damage": 15, "description": "The Shadow Lord fires a bolt of dark energy!"},
                    {"name": "Shadow Slash", "damage": 12, "description": "A blade of shadow cuts through the air!"},
                    {"name": "Soul Drain", "damage": 10, "description": "You feel your life force being drained!"},
                    {"name": "Dark Pulse", "damage": 18, "description": "A wave of darkness crashes over you!"}
                ]
            }
        }


    boss_z = layers - 1
    boss_placed = False
    for pos in atlas[boss_z]["position"]:
        if atlas[boss_z]["position"][pos] is None:
            atlas[boss_z]["position"][pos] = boss_id
            boss_placed = True
            break

    if not boss_placed:
        positions = [pos for pos in atlas[boss_z]["position"].keys()]
        atlas[boss_z]["position"][random.choice(positions)] = boss_id

    character_file = "json_files/character.json"

    character_name = character.character_name()
    player_name = character.player_name()
    class_name = character.character_class("json_files/classes.json")
    character_data = character.create_character(character_name, player_name, character_file, class_name,
                                                class_data, items_data)

    map.display_map(character_data, atlas, events_by_id)
    map.describe_location(events_by_id, character_data, atlas)

    while character.is_alive(character_data):
        if not sound.is_alive():
            sound = playsound("sounds/nube_negra_shiro_sagisu.mp3", block=False)

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

            if event_id == 11 and character_z < layers - 1:
                stairs_choice = input("Stairs detected. Go down? (y/n): ").strip().lower()
                if stairs_choice == 'y':
                    character_data = map.traverse_stairs(character_data, "down", atlas)
                    map.display_map(character_data, atlas, events_by_id)
                    map.describe_location(events_by_id, character_data, atlas)
                    continue
            elif event_id == boss_id:
                print("\n" + "=" * 50)
                print("BOSS ENCOUNTER!")
                print("=" * 50)

                boss_event = events_by_id[boss_id]
                boss_enemy = boss_event["enemy"]

                temp_enemy = dict(boss_enemy)
                combat_result = combat.boss_combat(character_data, temp_enemy, class_data, items_data)

                if combat_result:
                    print(f"\nCongratulations! You defeated the {boss_enemy['name']}!")
                    print("You have conquered this dungeon!")

                    atlas[character_z]["position"][(character_y, character_x)] = None

                    character_data = progression.award_xp(character_data, 200, class_data, items_data)

                    continue_choice = input("\nDo you want to continue exploring? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        print("Thanks for playing!")
                        break
                else:
                    print(f"\nYou were defeated by the {boss_enemy['name']}...")
                    print("Game Over!")
                    break

            elif events_by_id[event_id]["type"] == "fight":
                sound.stop()
                combat.combat(character_data, events_by_id, atlas, class_data, items_data)
                if character.is_alive(character_data):
                    atlas[character_z]["position"][(character_y, character_x)] = None
                    print("The area is now clear.")
                map.display_map(character_data, atlas, events_by_id)


            if not character.is_alive(character_data):
                print("Game Over! Your character has died.")
                break

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