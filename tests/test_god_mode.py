import unittest
from unittest.mock import patch
from game.game import god_mode


class TestGodMode(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "current": {
                    "health": 100
                }
            }
        }

    @patch("builtins.input", side_effect=["ffxiv"])
    def test_correct_code_activates_god_mode(self, mock_input):
        result = god_mode(self.character)

        self.assertEqual(result["character"]["current"]["health"], 9999)

    @patch("builtins.input", side_effect=["wrong", "n"])
    def test_wrong_code_no_hint_no_change(self, mock_input):
        result = god_mode(self.character)

        self.assertEqual(result["character"]["current"]["health"], 100)

    @patch("builtins.input", side_effect=["wrong", "y", "ffxiv"])
    def test_hint_then_correct_code(self, mock_input):
        result = god_mode(self.character)

        self.assertEqual(result["character"]["current"]["health"], 9999)

    @patch("builtins.input", side_effect=["wrong", "y", "wrong", "n"])
    def test_multiple_attempts_then_exit(self, mock_input):
        result = god_mode(self.character)

        self.assertEqual(result["character"]["current"]["health"], 100)


if __name__ == "__main__":
    unittest.main()