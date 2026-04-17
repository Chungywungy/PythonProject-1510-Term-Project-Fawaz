import unittest
from game.character import get_effective_stats


class TestGetEffectiveStats(unittest.TestCase):

    def setUp(self):
        self.base_character = {
            "character": {
                "base_stats": {
                    "strength": 10,
                    "constitution": 8
                },
                "trait_bonuses": {},
                "equipment": {}
            }
        }

        self.items_data = {
            "items": [
                {
                    "name": "Iron Sword",
                    "type": "equipment",
                    "stats": {"strength": 3}
                },
                {
                    "name": "Steel Armor",
                    "type": "equipment",
                    "stats": {"constitution": 5}
                }
            ]
        }

    def test_base_stats_only(self):
        result = get_effective_stats(self.base_character, self.items_data)
        self.assertEqual(result, {"strength": 10, "constitution": 8})

    def test_with_trait_bonus(self):
        character = self.base_character.copy()
        character["character"]["trait_bonuses"] = {
            "bonus1": {"strength": 2}
        }

        result = get_effective_stats(character, self.items_data)
        self.assertEqual(result, {"strength": 12, "constitution": 8})

    def test_with_equipment(self):
        character = self.base_character.copy()
        character["character"]["equipment"] = {
            "weapon": "Iron Sword"
        }

        result = get_effective_stats(character, self.items_data)
        self.assertEqual(result, {"strength": 13, "constitution": 8})

    def test_with_traits_and_equipment(self):
        character = self.base_character.copy()
        character["character"]["trait_bonuses"] = {
            "bonus1": {"strength": 2}
        }
        character["character"]["equipment"] = {
            "weapon": "Iron Sword"
        }

        result = get_effective_stats(character, self.items_data)
        self.assertEqual(result, {"strength": 15, "constitution": 8})

    def test_multiple_equipment(self):
        character = self.base_character.copy()
        character["character"]["equipment"] = {
            "weapon": "Iron Sword",
            "armor": "Steel Armor"
        }

        result = get_effective_stats(character, self.items_data)
        self.assertEqual(result, {"strength": 13, "constitution": 13})

    def test_ignore_nonexistent_item(self):
        character = self.base_character.copy()
        character["character"]["equipment"] = {
            "weapon": "Legendary Sword"  # not in items_data
        }

        result = get_effective_stats(character, self.items_data)
        self.assertEqual(result, {"strength": 10, "constitution": 8})

    def test_ignore_invalid_stat_from_item(self):
        items_data = {
            "items": [
                {
                    "name": "Weird Item",
                    "type": "equipment",
                    "stats": {"luck": 100}  # not in base stats
                }
            ]
        }

        character = self.base_character.copy()
        character["character"]["equipment"] = {
            "weapon": "Weird Item"
        }

        result = get_effective_stats(character, items_data)
        self.assertEqual(result, {"strength": 10, "constitution": 8})


if __name__ == '__main__':
    unittest.main()