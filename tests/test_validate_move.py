import unittest

from game.map import validate_move


class TestValidateMove(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "location": {
                    "character_x": 1,
                    "character_y": 1,
                    "character_z": 0
                }
            }
        }

        self.atlas = {
            0: {
                "position": {
                    (1, 0): 1,   # north
                    (2, 1): 2,   # east
                    (1, 2): 3,   # south
                    (0, 1): 4,   # west
                    (5, 5): None # empty tile (should be False)
                }
            }
        }

    def test_move_north_valid(self):
        result = validate_move(1, self.character, self.atlas)
        self.assertTrue(result)

    def test_move_east_valid(self):
        result = validate_move(2, self.character, self.atlas)
        self.assertTrue(result)

    def test_move_south_valid(self):
        result = validate_move(3, self.character, self.atlas)
        self.assertTrue(result)

    def test_move_west_valid(self):
        result = validate_move(4, self.character, self.atlas)
        self.assertTrue(result)

    def test_invalid_direction_returns_false(self):
        result = validate_move(99, self.character, self.atlas)
        self.assertFalse(result)

    def test_missing_tile_returns_false(self):
        # position exists but value is None → falsy
        character = {
            "character": {
                "location": {
                    "character_x": 4,
                    "character_y": 4,
                    "character_z": 0
                }
            }
        }

        result = validate_move(1, character, self.atlas)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()