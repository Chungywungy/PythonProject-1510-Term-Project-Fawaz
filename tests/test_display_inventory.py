import unittest
from unittest.mock import patch
from io import StringIO

from game.combat import display_inventory


class TestDisplayInventory(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_no_consumables(self, mock_stdout):
        character = {
            "character": {
                "inventory": [
                    {"name": "Sword", "type": "equipment"}
                ]
            }
        }

        display_inventory(character)

        self.assertIn("no consumable items", mock_stdout.getvalue().lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_single_consumable(self, mock_stdout):
        character = {
            "character": {
                "inventory": [
                    {"name": "Sword", "type": "equipment"},
                    {"name": "Potion", "type": "consumable"}
                ]
            }
        }

        display_inventory(character)

        output = mock_stdout.getvalue()
        self.assertIn("Inventory:", output)
        self.assertIn("1: Potion", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_multiple_consumables_ordered(self, mock_stdout):
        character = {
            "character": {
                "inventory": [
                    {"name": "Potion", "type": "consumable"},
                    {"name": "Elixir", "type": "consumable"},
                    {"name": "Sword", "type": "equipment"}
                ]
            }
        }

        display_inventory(character)

        output = mock_stdout.getvalue()

        self.assertIn("1: Potion", output)
        self.assertIn("2: Elixir", output)
        self.assertTrue(output.index("Potion") < output.index("Elixir"))

    @patch("sys.stdout", new_callable=StringIO)
    def test_only_equipment(self, mock_stdout):
        character = {
            "character": {
                "inventory": [
                    {"name": "Sword", "type": "equipment"}
                ]
            }
        }

        display_inventory(character)

        self.assertIn("no consumable items", mock_stdout.getvalue().lower())


if __name__ == "__main__":
    unittest.main()