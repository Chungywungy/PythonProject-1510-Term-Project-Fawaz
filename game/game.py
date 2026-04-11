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