import json


def open_json(file: str) -> dict:
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