# game/equipment.py

from game.colours import Colours, colourize
from game.character import equip_item, unequip_item, get_effective_stats


def display_equipment(character: dict) -> None:
    """Display currently equipped items."""
    equipment = character["character"]["equipment"]

    print(colourize("\n" + "=" * 50, Colours.TITLE))
    print(colourize("⚔️  CURRENT EQUIPMENT  ⚔️", Colours.TITLE))
    print(colourize("=" * 50, Colours.TITLE))

    slots = ["weapon", "offhand", "head", "chest", "legs", "feet"]
    slot_names = {
        "weapon": "Weapon",
        "offhand": "Off-hand",
        "head": "Head",
        "chest": "Chest",
        "legs": "Legs",
        "feet": "Feet"
    }

    for slot in slots:
        item = equipment.get(slot)
        if item:
            print(f"{slot_names[slot]}: {colourize(item, Colours.BUFF)}")
        else:
            print(f"{slot_names[slot]}: {colourize('Empty', Colours.WARNING)}")

    print("=" * 50)


def display_inventory_with_equipment(character: dict, items_data: dict) -> None:
    """Display inventory with equipment items marked."""
    inventory = character["character"]["inventory"]

    if len(inventory) == 0:
        print(colourize("\n📦 Your inventory is empty.", Colours.WARNING))
        return

    print(colourize("\n" + "=" * 50, Colours.TITLE))
    print(colourize("📦 INVENTORY", Colours.TITLE))
    print(colourize("=" * 50, Colours.TITLE))

    # Separate equipment and consumables
    equipment_items = []
    consumable_items = []

    for item in inventory:
        if item["type"] == "equipment":
            equipment_items.append(item)
        else:
            consumable_items.append(item)

    if equipment_items:
        print(colourize("\n⚔️  Equipment:", Colours.BUFF))
        for i, item in enumerate(equipment_items, 1):
            stats_str = ", ".join([f"+{v} {k}" for k, v in item["stats"].items()])
            print(f"  {i}. {colourize(item['name'], Colours.SPECIAL)} [{item['slot']}] - {stats_str}")

    if consumable_items:
        print(colourize("\n💊  Consumables:", Colours.HEAL))
        offset = len(equipment_items)
        for i, item in enumerate(consumable_items, offset + 1):
            if "heal" in item.get("effect", {}):
                print(f"  {i}. {colourize(item['name'], Colours.HEAL)} - Heals {item['effect']['heal']} HP")
            elif "damage" in item.get("effect", {}):
                print(f"  {i}. {colourize(item['name'], Colours.FAIL)} - Deals {item['effect']['damage']} damage")
            elif "xp" in item.get("effect", {}):
                print(f"  {i}. {colourize(item['name'], Colours.XP)} - +{item['effect']['xp']} XP")
            elif "attack_boost" in item.get("effect", {}):
                print(
                    f"  {i}. {colourize(item['name'], Colours.BUFF)} - +{item['effect']['attack_boost']} attack for {item['effect'].get('duration', 1)} turns")
            else:
                print(f"  {i}. {colourize(item['name'], Colours.CYAN)}")

    print("=" * 50)


def equipment_menu(character: dict, items_data: dict) -> dict:
    """
    Display equipment management menu and handle player choices.
    """
    while True:
        print(colourize("\n" + "=" * 50, Colours.TITLE))
        print(colourize("⚔️  EQUIPMENT MANAGEMENT  ⚔️", Colours.TITLE))
        print(colourize("=" * 50, Colours.TITLE))
        print("1. View Current Equipment")
        print("2. Equip Item from Inventory")
        print("3. Unequip Item")
        print("4. View Inventory")
        print("5. Return to Game")

        try:
            choice = int(input("\nEnter your choice: ").strip())
        except ValueError:
            print(colourize("Please enter a number.", Colours.FAIL))
            continue

        if choice == 1:
            display_equipment(character)

        elif choice == 2:
            character = equip_from_inventory(character, items_data)
            # Recalculate effective stats after equipment change
            effective = get_effective_stats(character, items_data)
            print(colourize("\n✨ Your stats have been updated!", Colours.BUFF))

        elif choice == 3:
            character = unequip_menu(character, items_data)
            effective = get_effective_stats(character, items_data)
            print(colourize("\n✨ Your stats have been updated!", Colours.BUFF))

        elif choice == 4:
            display_inventory_with_equipment(character, items_data)

        elif choice == 5:
            break

        else:
            print(colourize("Invalid choice. Please enter 1-5.", Colours.FAIL))

    return character


def equip_from_inventory(character: dict, items_data: dict) -> dict:
    """
    Allow player to select an equipment item from inventory to equip.
    """
    inventory = character["character"]["inventory"]
    equipment_items = [item for item in inventory if item["type"] == "equipment"]

    if len(equipment_items) == 0:
        print(colourize("\n📦 You have no equipment items in your inventory!", Colours.WARNING))
        return character

    print(colourize("\n" + "=" * 50, Colours.TITLE))
    print(colourize("⚔️  EQUIP ITEM  ⚔️", Colours.TITLE))
    print(colourize("=" * 50, Colours.TITLE))

    # Display equipment items
    items_by_slot = {}
    for i, item in enumerate(equipment_items, 1):
        slot = item["slot"]
        stats_str = ", ".join([f"+{v} {k}" for k, v in item["stats"].items()])

        # Check if something is already equipped in this slot
        current = character["character"]["equipment"].get(slot)
        current_str = f" (currently: {current})" if current else " (empty)"

        print(f"{i}. {colourize(item['name'], Colours.SPECIAL)} [{slot}]{current_str}")
        print(f"   Stats: {stats_str}")
        items_by_slot[i] = item

    print(f"{len(equipment_items) + 1}. Cancel")

    try:
        choice = int(input("\nSelect item to equip: ").strip())
    except ValueError:
        print(colourize("Invalid choice.", Colours.FAIL))
        return character

    if 1 <= choice <= len(equipment_items):
        item_to_equip = items_by_slot[choice]
        slot = item_to_equip["slot"]

        # Check if we need to unequip current item first
        current_item = character["character"]["equipment"].get(slot)
        if current_item:
            print(colourize(f"\n⚠️ You already have {current_item} equipped in the {slot} slot.", Colours.WARNING))
            confirm = input(f"Unequip {current_item} first? (y/n): ").strip().lower()
            if confirm == 'y':
                character = unequip_item(character, slot, items_data)
            else:
                print("Equipment cancelled.")
                return character

        # Equip the new item
        character = equip_item(character, item_to_equip["name"], items_data)

    elif choice == len(equipment_items) + 1:
        print("Equipment cancelled.")
    else:
        print(colourize("Invalid choice.", Colours.FAIL))

    return character


def unequip_menu(character: dict, items_data: dict) -> dict:
    """
    Allow player to select a slot to unequip.
    """
    equipment = character["character"]["equipment"]
    equipped_slots = {slot: item for slot, item in equipment.items() if item is not None}

    if len(equipped_slots) == 0:
        print(colourize("\n⚠️ You have nothing equipped!", Colours.WARNING))
        return character

    print(colourize("\n" + "=" * 50, Colours.TITLE))
    print(colourize("⚔️  UNEQUIP ITEM  ⚔️", Colours.TITLE))
    print(colourize("=" * 50, Colours.TITLE))

    slot_names = {
        "weapon": "Weapon",
        "offhand": "Off-hand",
        "head": "Head",
        "chest": "Chest",
        "legs": "Legs",
        "feet": "Feet"
    }

    slots_list = list(equipped_slots.keys())
    for i, slot in enumerate(slots_list, 1):
        item = equipped_slots[slot]
        print(f"{i}. {slot_names[slot]}: {colourize(item, Colours.BUFF)}")

    print(f"{len(slots_list) + 1}. Cancel")

    try:
        choice = int(input("\nSelect slot to unequip: ").strip())
    except ValueError:
        print(colourize("Invalid choice.", Colours.FAIL))
        return character

    if 1 <= choice <= len(slots_list):
        slot = slots_list[choice - 1]
        character = unequip_item(character, slot, items_data)
    elif choice == len(slots_list) + 1:
        print("Cancelled.")
    else:
        print(colourize("Invalid choice.", Colours.FAIL))

    return character