import unittest
from unittest.mock import patch

from game.map import get_user_choice


class TestGetUserChoice(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_valid_input_north(self, mock_print, mock_input):
        result = get_user_choice()
        self.assertEqual(result, 1)

    @patch("builtins.input", side_effect=["5", "2"])
    @patch("builtins.print")
    def test_invalid_then_valid_input(self, mock_print, mock_input):
        result = get_user_choice()
        self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["abc", "3"])
    @patch("builtins.print")
    def test_non_integer_then_valid(self, mock_print, mock_input):
        result = get_user_choice()
        self.assertEqual(result, 3)

    @patch("builtins.input", side_effect=["4"])
    @patch("builtins.print")
    def test_valid_input_west(self, mock_print, mock_input):
        result = get_user_choice()
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()