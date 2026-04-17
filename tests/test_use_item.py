import unittest
from unittest.mock import patch
from io import StringIO
import copy

from game.combat import use_item


class TestUseItem(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "inventory": [
                    {"name": "Sword", "type": "equipment"},
                    {"name": "Potion", "type": "consumable"}
                ]
            }
        }

        self.enemy = {
            "name": "Goblin",
            "health": 50
        }

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_consumables(self, mock_stdout):
        character = {
            "character": {
                "inventory": [
                    {"name": "Sword", "type": "equipment"}
                ]
            }
        }

        result_char, result_enemy = use_item(character, self.enemy)

        self.assertEqual(result_char, character)
        self.assertEqual(result_enemy, self.enemy)
        self.assertIn("no consumable items", mock_stdout.getvalue().lower())

    @patch("builtins.input", side_effect=["0"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_cancel_use_item(self, mock_stdout, mock_input):
        character = copy.deepcopy(self.character)

        result_char, result_enemy = use_item(character, self.enemy)

        self.assertEqual(result_char, character)
        self.assertEqual(result_enemy, self.enemy)
        self.assertIn("put your bag away", mock_stdout.getvalue().lower())

    @patch("builtins.input", side_effect=["1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_use_valid_item(self, mock_stdout, mock_input):
        character = copy.deepcopy(self.character)

        # mock apply_item_effect so we don't depend on it
        with patch("game.combat.apply_item_effect", side_effect=lambda c, i, e: c):
            result_char, result_enemy = use_item(character, self.enemy)

        inventory_names = [i["name"] for i in result_char["character"]["inventory"]]

        self.assertNotIn("Potion", inventory_names)
        self.assertEqual(result_enemy, self.enemy)

    @patch("builtins.input", side_effect=["abc", "0"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_input_then_cancel(self, mock_stdout, mock_input):
        character = copy.deepcopy(self.character)

        result_char, result_enemy = use_item(character, self.enemy)

        self.assertIn("please enter an integer", mock_stdout.getvalue().lower())


if __name__ == "__main__":
    unittest.main()