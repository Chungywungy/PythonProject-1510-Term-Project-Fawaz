from random import randint

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


def combat():
    pass


def enemy_behaviour():
    pass


def boss_behaviour():
    pass


def main():
    pass


if __name__ == '__main__':
    main()