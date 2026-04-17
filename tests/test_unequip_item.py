import unittest
from unittest.mock import patch
import copy
from game.character import unequip_item


class TestUnequipItem(unittest.TestCase):

    def setUp(self):
        self.items_data = {
            "items": [
                {
                    "name": "Iron Sword",
                    "type": "equipment",
                    "slot": "weapon",
                    "stats": {"strength": 3}
                },
                {
                    "name": "Leather Armor",
                    "type": "equipment",
                    "slot": "armor",
                    "stats": {"constitution": 2}
                }
            ]
        }

        self.character = {
            "character": {
                "name": "Amon",
                "inventory": [],
                "equipment": {
                    "weapon": None,
                    "armor": None
                }
            }
        }

    @patch('builtins.print')
    def test_unequip_item_success(self, mock_print):
        character = copy.deepcopy(self.character)

        character["character"]["equipment"]["weapon"] = "Iron Sword"

        result = unequip_item(character, "weapon", self.items_data)

        # item moved to inventory
        self.assertTrue(
            any(i["name"] == "Iron Sword" for i in result["character"]["inventory"])
        )

        # slot cleared
        self.assertIsNone(result["character"]["equipment"]["weapon"])

    @patch('builtins.print')
    def test_unequip_empty_slot(self, mock_print):
        character = copy.deepcopy(self.character)

        result = unequip_item(character, "weapon", self.items_data)

        self.assertEqual(result, character)
        mock_print.assert_called_with("Nothing equipped in weapon.")

    @patch('builtins.print')
    def test_unequip_armor_success(self, mock_print):
        character = copy.deepcopy(self.character)
        character["character"]["equipment"]["armor"] = "Leather Armor"

        result = unequip_item(character, "armor", self.items_data)

        self.assertTrue(
            any(i["name"] == "Leather Armor" for i in result["character"]["inventory"])
        )
        self.assertIsNone(result["character"]["equipment"]["armor"])

    @patch('builtins.print')
    def test_inventory_item_structure(self, mock_print):
        character = copy.deepcopy(self.character)
        character["character"]["equipment"]["weapon"] = "Iron Sword"

        result = unequip_item(character, "weapon", self.items_data)

        item = result["character"]["inventory"][0]

        self.assertEqual(item["name"], "Iron Sword")
        self.assertEqual(item["type"], "equipment")
        self.assertEqual(item["slot"], "weapon")
        self.assertEqual(item["stats"], {"strength": 3})


if __name__ == "__main__":
    unittest.main()