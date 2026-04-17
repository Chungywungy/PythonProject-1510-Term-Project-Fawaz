def award_xp(character: dict, amount: int, class_data: dict, items_data: dict) -> dict:
    """
    Award experience points to a character and handle level-ups when thresholds are reached.

    The function adds the given XP amount to the character's total experience.
    It then checks if the character has reached the XP threshold required for
    the next level. If so, the character is leveled up using the level_up function.

    XP thresholds are defined for each level (e.g., level 2 requires 100 XP,
    level 3 requires 300 XP).

    :param character: A dictionary containing character data, including level and xp
    :param amount: The amount of XP to award
    :param class_data: A dictionary containing class definitions for level-up logic
    :param items_data: A dictionary containing item data used during level-up
    :precondition: character contains "xp" and "level" keys
                   amount is a non-negative integer
    :postcondition: increase character's XP and level up if thresholds are met
    :returns: the updated character dictionary
    """
    xp_thresholds = {2: 100, 3: 300}

    character["character"]["xp"] += amount
    print(f"You gained {amount} xp! | Total: {character['character']['xp']} xp")

    current_level = character["character"]["level"]
    next_level = current_level + 1

    if next_level in xp_thresholds and character["character"]["xp"] >= xp_thresholds[next_level]:
        character = level_up(character, class_data, items_data)

    return character