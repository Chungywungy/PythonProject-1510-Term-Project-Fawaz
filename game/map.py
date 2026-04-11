import random


def build_map(layers, rows, columns):
    atlas = dict()
    for layer in range(layers + 1):
        atlas[layer] = {"position": {}}
        for row in range(rows + 1):
            for column in range(columns + 1):
                atlas[layer]["position"][(row, column)] = random.choice(range(1, 11))

    return atlas


def display_map():
    pass


def describe_location():
    pass


def character_direction():
    pass


def move_character():
    pass


def validate_move():
    pass


def main():
    pass


if __name__ == '__main__':
    main()