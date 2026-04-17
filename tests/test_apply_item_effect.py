import unittest
from unittest.mock import patch
from io import StringIO
import copy

from game.combat import apply_item_effect


class TestApplyItemEffect(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "base_stats": {
                    "constitution": 10
                },
                "derived_stats": {
                    "max_health": {"multiplier": 2}
                },
                "current": {
                    "health": 10
                }
            }
        }

        self.enemy = {
            "name": "Goblin",
            "health": 50
        }

    @patch("sys.stdout", new_callable=StringIO)
    def test_heal_item(self, mock_stdout):
        character = copy.deepcopy(self.character)

        item = {
            "name": "Potion",
            "effect": {
                "heal": 20
            }
        }

        result_char, _ = apply_item_effect(character, item, self.enemy)

        self.assertGreaterEqual(result_char["character"]["current"]["health"], 10)
        self.assertIn("recover", mock_stdout.getvalue().lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_damage_enemy(self, mock_stdout):
        character = copy.deepcopy(self.character)

        item = {
            "name": "Bomb",
            "effect": {
                "damage": 15,
                "target": "enemy"
            }
        }

        result_char, result_enemy = apply_item_effect(character, item, self.enemy)

        self.assertEqual(result_enemy["health"], 35)
        self.assertIn("takes", mock_stdout.getvalue().lower())

    @patch("sys.stdout", new_callable=StringIO)
    def test_damage_self(self, mock_stdout):
        character = copy.deepcopy(self.character)

        item = {
            "name": "Cursed Herb",
            "effect": {
                "damage": 5,
                "target": "self"
            }
        }

        result_char, _ = apply_item_effect(character, item, self.enemy)

        self.assertEqual(result_char["character"]["current"]["health"], 5)

    @patch("sys.stdout", new_callable=StringIO)
    def test_xp_gain(self, mock_stdout):
        character = copy.deepcopy(self.character)

        item = {
            "name": "XP Scroll",
            "effect": {
                "xp": 50
            }
        }

        result_char, _ = apply_item_effect(character, item, self.enemy)

        self.assertEqual(result_char["character"]["pending_xp"], 50)

    @patch("sys.stdout", new_callable=StringIO)
    def test_attack_boost_applied(self, mock_stdout):
        character = copy.deepcopy(self.character)

        item = {
            "name": "Strength Potion",
            "effect": {
                "attack_boost": 5,
                "duration": 3
            }
        }

        result_char, _ = apply_item_effect(character, item, self.enemy)

        buffs = result_char["character"]["temp_buffs"]
        self.assertIn("attack_boost", buffs)
        self.assertEqual(buffs["attack_boost"]["amount"], 5)
        self.assertEqual(buffs["attack_boost"]["turns_remaining"], 3)


if __name__ == "__main__":
    unittest.main()