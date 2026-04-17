import json


def open_json(file: str) -> dict:
    """
    Load and return the contents of a JSON file as a dictionary.

    The function checks that the file has a `.json` extension and attempts
    to parse it. If the file is not valid JSON or is empty, a ValueError
    is raised.

    :param file: The path to the JSON file as string
    :precondition: file is a valid path to a JSON file as a string
    :postcondition: convert the JSON file to a dictionary
    :returns: the contents of the JSON file as a dictionary
    :raises ValueError: if the JSON file is empty or if the file is invalid
    """
    if ".json" not in file:
        raise ValueError("File is not a JSON file.")
    else:
        with open(file, 'r') as file_object:
            try:
                character_data = json.load(file_object)
            except json.JSONDecodeError:
                raise ValueError("The JSON file is empty.")
            else:
                return character_data


def main():
    return


if __name__ == '__main__':
    main()