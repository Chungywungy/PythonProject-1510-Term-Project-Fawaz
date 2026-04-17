import unittest
from unittest.mock import patch
from io import StringIO
import copy

from game.combat import perform_action


class TestPerformAction(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "name": "Hero",
                "base_stats": {
                    "strength": 10
                },
                "current": {
                    "mana": 10,
                    "health": 20
                },
                "derived_stats": {
                    "max_health": {"multiplier": 2}
                }
            }
        }

        self.enemy = {
            "name": "Goblin",
            "health": 50
        }

        self.action_attack = {
            "name": "Strike",
            "type": "attack",
            "mana_cost": 2,
            "cooldown": 3,
            "scaling": {
                "stat": "strength",
                "multiplier": 2
            }
        }

        self.action_buff = {
            "name": "Buff",
            "type": "buff",
            "mana_cost": 1,
            "cooldown": 2
        }

    @patch("sys.stdout", new_callable=StringIO)
    def test_attack_reduces_enemy_health(self, mock_stdout):
        character = copy.deepcopy(self.character)
        enemy = copy.deepcopy(self.enemy)
        cooldowns = {}

        result_enemy, result_cd = perform_action(
            character, enemy, "strike", self.action_attack, cooldowns
        )

        self.assertEqual(result_enemy["health"], 30)
        self.assertIn("damage", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_mana_reduced(self, mock_stdout):
        character = copy.deepcopy(self.character)
        enemy = copy.deepcopy(self.enemy)
        cooldowns = {}

        perform_action(character, enemy, "strike", self.action_attack, cooldowns)

        self.assertEqual(character["character"]["current"]["mana"], 8)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cooldown_applied(self, mock_stdout):
        character = copy.deepcopy(self.character)
        enemy = copy.deepcopy(self.enemy)
        cooldowns = {}

        _, result_cd = perform_action(
            character, enemy, "strike", self.action_attack, cooldowns
        )

        self.assertIn("strike", result_cd)
        self.assertEqual(result_cd["strike"], 3)

    @patch("sys.stdout", new_callable=StringIO)
    def test_non_attack_action(self, mock_stdout):
        character = copy.deepcopy(self.character)
        enemy = copy.deepcopy(self.enemy)
        cooldowns = {}

        result_enemy, result_cd = perform_action(
            character, enemy, "buff", self.action_buff, cooldowns
        )

        self.assertEqual(result_enemy["health"], 50)
        self.assertIn("Effect not implemented yet", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()