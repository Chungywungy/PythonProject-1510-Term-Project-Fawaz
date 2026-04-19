import random
import time

from playsound3 import playsound

from game import character, file_tampering, map, combat, progression
from game.colours import Colours, colourize
from game.boss_manager import save_character_as_boss, load_previous_boss, has_previous_boss
from game.events import handle_chest, handle_boon, handle_debuff, apply_status_effects
from game.equipment import equipment_menu, display_equipment


def management_menu(character: dict, items_data: dict) -> dict:
    """Display management menu for equipment and inventory."""
    while True:
        print(colourize("\n" + "=" * 50, Colours.TITLE))
        print(colourize("🏕️  MANAGEMENT  🏕️", Colours.TITLE))
        print(colourize("=" * 50, Colours.TITLE))
        print("1. Manage Equipment")
        print("2. View Stats")
        print("3. Continue Journey")

        try:
            choice = int(input("\nEnter your choice: ").strip())
        except ValueError:
            print(colourize("Please enter a number.", Colours.FAIL))
            continue

        if choice == 1:
            character = equipment_menu(character, items_data)
        elif choice == 2:
            display_character_stats(character, items_data)
        elif choice == 3:
            break
        else:
            print(colourize("Invalid choice.", Colours.FAIL))

    return character


def display_character_stats(character: dict, items_data: dict) -> None:
    """Display character's current stats."""
    from game.character import get_effective_stats
    effective = get_effective_stats(character, items_data)

    print(colourize("\n" + "=" * 50, Colours.TITLE))
    print(colourize(f"📜 {character['character']['name']}'s STATS", Colours.TITLE))
    print(colourize("=" * 50, Colours.TITLE))

    print(f"\n{colourize('Class:', Colours.BUFF)} {character['character']['class']}")
    print(f"{colourize('Level:', Colours.BUFF)} {character['character']['level']}")
    print(f"{colourize('XP:', Colours.BUFF)} {character['character']['xp']}")

    print(colourize("\n📊 Base Stats:", Colours.CYAN))
    for stat, value in character["character"]["base_stats"].items():
        effective_value = effective.get(stat, value)
        if effective_value != value:
            print(
                f"  {stat.capitalize()}: {value} → {colourize(f'+{effective_value - value}', Colours.HEAL)} (Total: {effective_value})")
        else:
            print(f"  {stat.capitalize()}: {value}")

    # Current health/mana
    max_health = effective["constitution"] * character["character"]["derived_stats"]["max_health"]["multiplier"]
    max_mana = effective["intellect"] * character["character"]["derived_stats"]["max_mana"]["multiplier"]

    print(colourize("\n❤️ Health:", Colours.HP))
    print(f"   {character['character']['current']['health']}/{max_health}")

    print(colourize("\n💙 Mana:", Colours.MANA))
    print(f"   {character['character']['current']['mana']}/{max_mana}")

    # Equipment summary
    print(colourize("\n⚔️ Equipment:", Colours.BUFF))
    equipment = character["character"]["equipment"]
    for slot, item in equipment.items():
        if item:
            print(f"  {slot.capitalize()}: {item}")
        else:
            print(f"  {slot.capitalize()}: Empty")

    print("=" * 50)


def god_mode(character_data: dict) -> dict:
    """
    Prompt the user to enter a secret code to activate god mode for the character.

    The function repeatedly asks the user to guess the name of a specific MMO.
    If the correct answer ("ffxiv") is provided, the character's health is set
    to a very high value (9999), effectively enabling god mode. If the user
    answers incorrectly, they may request a hint or exit the prompt.

    :param character_data: a dictionary containing the character's full data,
                           including nested "character" -> "current" -> "health"
    :precondition: character_data contains valid nested keys for modifying health
    :postcondition: enter the correct code and the character's health will be set
                    to 9999; otherwise, no changes are made
    :returns: the updated character_data dictionary
    """
    while True:
        secret_code = str(input("\nWhat is the name of the best mmo ever? ")).lower().strip()
        if secret_code == "ffxiv":
            character_data["character"]["current"]["health"] = 9999
            print("God mode activated")
            break
        else:
            hint = str(input("Would you like a hint? (y/n) ")).lower().strip()
            if hint == "y":
                print("Hint: It's not WoW :)")
                continue
            else:
                print("\nEnjoy the game!")
                break
    return character_data


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
    sound = playsound("sounds/test.mp3", block=False)

    rows = 5
    columns = 5
    layers = 4

    atlas = map.build(layers, rows, columns)
    events = file_tampering.open_json("json_files/events.json")
    events_by_id = {event["id"]: event for event in events["events"]}
    class_data = file_tampering.open_json("json_files/classes.json")
    items_data = file_tampering.open_json("json_files/items.json")

    boss_id = 12

    saved_boss = load_previous_boss()

    if saved_boss:
        events_by_id[boss_id] = saved_boss
        print(colourize(f"\n⚠️ A dark presence lingers in the depths...", Colours.WARNING))
        print(colourize(f"   The shadow of {saved_boss['enemy']['original_player_name']} awaits!", Colours.SPECIAL))
        time.sleep(2)
    else:
        events_by_id[boss_id] = {
            "id": 12,
            "type": "boss",
            "name": "Shadow Lord",
            "description": "The Shadow Lord stands before you, radiating dark energy!",
            "enemy": {
                "name": "Shadow Lord",
                "health": 200,
                "attacks": [
                    {"name": "Dark Bolt", "damage": 37, "description": "The Shadow Lord fires a bolt of dark energy!"},
                    {"name": "Shadow Slash", "damage": 40, "description": "A blade of shadow cuts through the air!"},
                    {"name": "Soul Drain", "damage": 50, "description": "You feel your life force being drained!"},
                    {"name": "Dark Pulse", "damage": 67, "description": "A wave of darkness crashes over you!"}
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

    print(colourize("\nChosen by forces long forgotten, you descend as a lone knight into the Eternal Dungeon.\n"
                   "Beneath its endless layers, a living darkness stirs, corrupting all it touches.\n"
                   "Steel your resolve. You are the last light it has yet to consume.", Colours.TITLE), flush=True)
    time.sleep(5)

    character_data = character.create_character(character_name, player_name, character_file, class_name,
                                                class_data, items_data)
    character_data = god_mode(character_data)

    map.display_map(character_data, atlas, events_by_id)
    map.describe_location(events_by_id, character_data, atlas)

    print(colourize("\n[E] to manage equipment | [Any key] to continue", Colours.CYAN))
    manage_choice = input().strip().lower()
    if manage_choice == 'e':
        character_data = management_menu(character_data, items_data)
        # Redisplay map after management
        map.display_map(character_data, atlas, events_by_id)
        map.describe_location(events_by_id, character_data, atlas)

    while character.is_alive(character_data):
        if not sound.is_alive():
            sound = playsound("sounds/test.mp3", block=False)

        print(colourize("\n[E] to manage equipment | [Any key] to continue", Colours.CYAN))
        manage_choice = input().strip().lower()
        if manage_choice == 'e':
            character_data = management_menu(character_data, items_data)
            # Redisplay map after management
            map.display_map(character_data, atlas, events_by_id)
            map.describe_location(events_by_id, character_data, atlas)


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

            character_data = apply_status_effects(character_data)

            if not character.is_alive(character_data):
                print(colourize("\nGame Over! Your character has died from lingering effects.", Colours.FAIL))
                break

            if event_id is None:
                # Empty tile, nothing happens
                continue

            if event_id == 11 and character_z < layers - 1:
                stairs_choice = input("\nStairs detected. Go down? (y/n): ").strip().lower()
                if stairs_choice == 'y':
                    character_data = map.traverse_stairs(character_data, "down", atlas)
                    map.display_map(character_data, atlas, events_by_id)
                    map.describe_location(events_by_id, character_data, atlas)
                    continue

            elif event_id == boss_id:
                sound.stop()
                print(colourize("\n" + "=" * 50, Colours.TITLE))
                print(colourize("BOSS ENCOUNTER!", Colours.FAIL))
                print(colourize("=" * 50, Colours.TITLE))

                boss_event = events_by_id[boss_id]
                boss_enemy = boss_event["enemy"]

                temp_enemy = dict(boss_enemy)
                combat_result = combat.boss_combat(character_data, temp_enemy, class_data, items_data)

                if combat_result:
                    print(colourize(f"\n✨ Congratulations! You defeated the {boss_enemy['name']}!", Colours.TITLE))
                    print(colourize("You have conquered this dungeon!", Colours.TITLE))

                    # Save this character as the next boss with class data
                    from game.boss_manager import save_character_as_boss
                    save_character_as_boss(character_data, class_data)

                    atlas[character_z]["position"][(character_y, character_x)] = None

                    character_data = progression.award_xp(character_data, 200, class_data, items_data)

                    continue_choice = input(
                        colourize("\nDo you want to continue exploring? (y/n): ", Colours.CYAN)).strip().lower()
                    if continue_choice != 'y':
                        print(colourize("\nThanks for playing!", Colours.TITLE))
                        break

            elif events_by_id[event_id]["type"] == "fight":
                sound.stop()
                combat.combat(character_data, events_by_id, atlas, class_data, items_data)
                if character.is_alive(character_data):
                    atlas[character_z]["position"][(character_y, character_x)] = None
                    print(colourize("\n✨ The area is now clear.", Colours.HEAL))
                map.display_map(character_data, atlas, events_by_id)

            elif events_by_id[event_id]["type"] == "chest":
                # Handle chest event
                character_data = handle_chest(character_data, events_by_id[event_id], items_data)
                # Mark chest as opened
                atlas[character_z]["position"][(character_y, character_x)] = None

                # Check if character died from trap
                if not character.is_alive(character_data):
                    print(colourize("\nGame Over! The chest proved fatal.", Colours.FAIL))
                    break

            elif events_by_id[event_id]["type"] == "boon":
                # Handle boon event
                character_data = handle_boon(character_data, events_by_id[event_id], class_data, items_data)
                # Boons are one-time use
                atlas[character_z]["position"][(character_y, character_x)] = None


            elif events_by_id[event_id]["type"] == "debuff":
                # Handle debuff event
                character_data = handle_debuff(character_data, events_by_id[event_id])
                # Debuffs are one-time triggers
                atlas[character_z]["position"][(character_y, character_x)] = None

                if not character.is_alive(character_data):
                    print(colourize("\nGame Over! The curse was too much to bear.", Colours.FAIL))
                    break

            if not character.is_alive(character_data):
                print("Game Over! Your character has died.")
                break

        else:
            map.display_map(character_data, atlas, events_by_id)
            print("\nYou can't go that way. Try again")
    return


def main():
    """
    Drive the program.
    """
    game()


if __name__ == '__main__':
    main()
