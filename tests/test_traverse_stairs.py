import unittest
from unittest.mock import patch
from io import StringIO
import copy

from game.map import traverse_stairs


class TestTraverseStairs(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "location": {
                    "character_z": 1
                }
            }
        }

        self.atlas = {
            0: {},
            1: {},
            2: {}
        }

    @patch("sys.stdout", new_callable=StringIO)
    def test_descend_valid(self, mock_stdout):
        character = copy.deepcopy(self.character)

        result = traverse_stairs(character, "down", self.atlas)

        self.assertEqual(result["character"]["location"]["character_z"], 2)
        self.assertIn("descend", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_ascend_valid(self, mock_stdout):
        character = copy.deepcopy(self.character)

        result = traverse_stairs(character, "up", self.atlas)

        self.assertEqual(result["character"]["location"]["character_z"], 0)
        self.assertIn("ascend", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_direction(self, mock_stdout):
        character = copy.deepcopy(self.character)

        result = traverse_stairs(character, "left", self.atlas)

        self.assertEqual(result["character"]["location"]["character_z"], 1)
        self.assertIn("can't go", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_cannot_descend_below_bottom(self, mock_stdout):
        character = copy.deepcopy(self.character)
        character["character"]["location"]["character_z"] = 2

        result = traverse_stairs(character, "down", self.atlas)

        self.assertEqual(result["character"]["location"]["character_z"], 2)
        self.assertIn("can't go", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_cannot_ascend_above_top(self, mock_stdout):
        character = copy.deepcopy(self.character)
        character["character"]["location"]["character_z"] = 0

        result = traverse_stairs(character, "up", self.atlas)

        self.assertEqual(result["character"]["location"]["character_z"], 0)
        self.assertIn("can't go", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()