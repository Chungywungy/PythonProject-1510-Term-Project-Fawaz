import unittest
from unittest.mock import patch
from io import StringIO
from game.map import describe_location


class TestDescribeLocation(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "location": {
                    "character_x": 0,
                    "character_y": 0,
                    "character_z": 0
                }
            }
        }

    @patch("sys.stdout", new_callable=StringIO)
    def test_empty_ground(self, mock_stdout):
        atlas = {0: {"position": {(0, 0): None}}}
        events = {}

        describe_location(events, self.character, atlas)

        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "You are standing on empty ground."
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_stairs(self, mock_stdout):
        atlas = {0: {"position": {(0, 0): 11}}}
        events = {}

        describe_location(events, self.character, atlas)

        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "Stairs leading to the next floor are here."
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_event_description(self, mock_stdout):
        atlas = {0: {"position": {(0, 0): 1}}}
        events = {1: {"description": "A dusty chest."}}

        describe_location(events, self.character, atlas)

        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "A dusty chest."
        )

    def test_missing_location_raises_keyerror(self):
        bad_character = {"character": {}}
        atlas = {0: {"position": {(0, 0): 1}}}
        events = {1: {"description": "test"}}

        with self.assertRaises(KeyError):
            describe_location(events, bad_character, atlas)


if __name__ == "__main__":
    unittest.main()