def character_name():
    mc_name = str(input("What is your characters' name? ").strip().title())

    while True:
        if len(mc_name) == 0:
            validate = str(input("The default name is Amon. Are you sure about your choice? (y/n) ")).strip().lower()
            if validate == 'y':
                mc_name = 'Amon'
                break
            elif validate == 'n':
                mc_name = str(input("What is your characters' name? ").strip().title())
                continue
            else:
                print("Please input 'y' or 'n'.")
                continue
        else:
            validate = str(
                input(f"Your character's name is {mc_name}. Are you sure about that? (y/n) ")).strip().lower()
            if validate == 'y':
                break
            elif validate == 'n':
                mc_name = str(input("What is your characters' name? ").strip().title())
                continue
            else:
                print("Please input 'y' or 'n'.")
                continue
    return mc_name


def player_name():
    pass


def create_character():
    pass


def is_alive():
    pass


def validate_player_name():
    pass


def character_class():
    pass


def validate_class():
    pass


def equip_item():
    pass


def validate_equip():
    pass


def see_inventory():
    pass


def level_up():
    pass


def main():
    pass


if __name__ == '__main__':
    main()