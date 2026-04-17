import unittest
import copy

from game.map import move_character


class TestMoveCharacter(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "location": {
                    "character_x": 0,
                    "character_y": 0
                }
            }
        }

    def test_move_north(self):
        character = copy.deepcopy(self.character)

        result = move_character(character, 1)

        self.assertEqual(result["character"]["location"]["character_y"], -1)
        self.assertEqual(result["character"]["location"]["character_x"], 0)

    def test_move_east(self):
        character = copy.deepcopy(self.character)

        result = move_character(character, 2)

        self.assertEqual(result["character"]["location"]["character_x"], 1)
        self.assertEqual(result["character"]["location"]["character_y"], 0)

    def test_move_south(self):
        character = copy.deepcopy(self.character)

        result = move_character(character, 3)

        self.assertEqual(result["character"]["location"]["character_y"], 1)
        self.assertEqual(result["character"]["location"]["character_x"], 0)

    def test_move_west(self):
        character = copy.deepcopy(self.character)

        result = move_character(character, 4)

        self.assertEqual(result["character"]["location"]["character_x"], -1)
        self.assertEqual(result["character"]["location"]["character_y"], 0)

    def test_invalid_direction_defaults_to_west(self):
        character = copy.deepcopy(self.character)

        result = move_character(character, 999)

        # falls into else branch → west movement
        self.assertEqual(result["character"]["location"]["character_x"], -1)


if __name__ == "__main__":
    unittest.main()