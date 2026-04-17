import unittest
from unittest.mock import patch
import copy

from game.character import award_xp


class TestAwardXP(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "xp": 0,
                "level": 1
            }
        }

        self.class_data = {}
        self.items_data = {}

    @patch('builtins.print')
    def test_gain_xp_no_level_up(self, mock_print):
        character = copy.deepcopy(self.character)

        result = award_xp(character, 50, self.class_data, self.items_data)

        self.assertEqual(result["character"]["xp"], 50)
        self.assertEqual(result["character"]["level"], 1)

    @patch('builtins.print')
    @patch('game.character.level_up')
    def test_level_up_triggered(self, mock_level_up, mock_print):
        character = copy.deepcopy(self.character)

        mock_level_up.side_effect = lambda c, d, i: c

        result = award_xp(character, 100, self.class_data, self.items_data)

        mock_level_up.assert_called_once()
        self.assertEqual(result["character"]["xp"], 100)

    @patch('builtins.print')
    @patch('game.character.level_up')
    def test_no_level_up_below_threshold(self, mock_level_up, mock_print):
        character = copy.deepcopy(self.character)

        award_xp(character, 99, self.class_data, self.items_data)

        mock_level_up.assert_not_called()

    @patch('builtins.print')
    @patch('game.character.level_up')
    def test_exact_threshold_level_2(self, mock_level_up, mock_print):
        character = copy.deepcopy(self.character)

        mock_level_up.side_effect = lambda c, d, i: c

        award_xp(character, 100, self.class_data, self.items_data)

        mock_level_up.assert_called_once()

    @patch('builtins.print')
    @patch('game.character.level_up')
    def test_level_up_called_only_once(self, mock_level_up, mock_print):
        character = copy.deepcopy(self.character)

        mock_level_up.side_effect = lambda c, d, i: c

        award_xp(character, 500, self.class_data, self.items_data)

        mock_level_up.assert_called_once()


if __name__ == "__main__":
    unittest.main()