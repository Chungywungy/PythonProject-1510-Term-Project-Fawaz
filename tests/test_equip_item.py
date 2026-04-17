import unittest
from unittest.mock import patch
import copy

from game.character import equip_item


class TestEquipItem(unittest.TestCase):

    def setUp(self):
        self.items_data = {
            "items": [
                {
                    "name": "Iron Sword",
                    "type": "equipment",
                    "slot": "weapon"
                },
                {
                    "name": "Leather Armor",
                    "type": "equipment",
                    "slot": "armor"
                },
                {
                    "name": "Apple",
                    "type": "consumable",
                    "slot": None
                }
            ]
        }

        self.character = {
            "character": {
                "name": "Amon",
                "inventory": [
                    {"name": "Iron Sword"},
                    {"name": "Leather Armor"},
                    {"name": "Apple"}
                ],
                "equipment": {
                    "weapon": None,
                    "armor": None
                }
            }
        }

    @patch('builtins.print')
    def test_equip_item_success(self, mock_print):
        character = copy.deepcopy(self.character)

        result = equip_item(character, "Iron Sword", self.items_data)

        self.assertEqual(result["character"]["equipment"]["weapon"], "Iron Sword")
        self.assertNotIn(
            {"name": "Iron Sword"},
            result["character"]["inventory"]
        )

    @patch('builtins.print')
    def test_item_not_found(self, mock_print):
        character = copy.deepcopy(self.character)

        with self.assertRaises(ValueError) as context:
            equip_item(character, "Fake Sword", self.items_data)

        self.assertIn("not found", str(context.exception))

    @patch('builtins.print')
    def test_item_not_equipment(self, mock_print):
        character = copy.deepcopy(self.character)

        with self.assertRaises(ValueError) as context:
            equip_item(character, "Apple", self.items_data)

        self.assertIn("not an equippable", str(context.exception))

    @patch('builtins.print')
    def test_item_not_in_inventory(self, mock_print):
        character = copy.deepcopy(self.character)
        character["character"]["inventory"] = []

        with self.assertRaises(ValueError) as context:
            equip_item(character, "Iron Sword", self.items_data)

        self.assertIn("not in", str(context.exception))

    @patch('builtins.print')
    @patch('game.character.unequip_item')
    def test_replace_equipped_item(self, mock_unequip, mock_print):
        mock_unequip.side_effect = lambda c, slot, data: c

        character = copy.deepcopy(self.character)
        character["character"]["equipment"]["weapon"] = "Old Sword"

        result = equip_item(character, "Iron Sword", self.items_data)

        mock_unequip.assert_called_once()
        self.assertEqual(result["character"]["equipment"]["weapon"], "Iron Sword")


if __name__ == "__main__":
    unittest.main()