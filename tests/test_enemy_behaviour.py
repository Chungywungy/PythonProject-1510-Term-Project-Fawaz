import unittest
from unittest.mock import patch
from io import StringIO

from game.combat import enemy_behaviour


class TestEnemyBehaviour(unittest.TestCase):

    @patch("random.choice")
    @patch("sys.stdout", new_callable=StringIO)
    def test_enemy_attack_reduces_health(self, mock_stdout, mock_choice):
        character = {
            "character": {
                "current": {
                    "health": 100
                }
            }
        }

        enemy = {
            "attacks": [
                {"damage": 20, "description": "Slash"},
                {"damage": 10, "description": "Punch"}
            ]
        }

        # force chosen attack
        mock_choice.return_value = enemy["attacks"][0]

        result = enemy_behaviour(character, enemy)

        self.assertEqual(result["character"]["current"]["health"], 80)
        self.assertIn("slash", mock_stdout.getvalue().lower())
        self.assertIn("you take 20 damage", mock_stdout.getvalue().lower())

    @patch("random.choice")
    @patch("sys.stdout", new_callable=StringIO)
    def test_enemy_attack_different_attack(self, mock_stdout, mock_choice):
        character = {
            "character": {
                "current": {
                    "health": 50
                }
            }
        }

        enemy = {
            "attacks": [
                {"damage": 5, "description": "Bite"}
            ]
        }

        mock_choice.return_value = enemy["attacks"][0]

        result = enemy_behaviour(character, enemy)

        self.assertEqual(result["character"]["current"]["health"], 45)
        self.assertIn("bite", mock_stdout.getvalue().lower())


if __name__ == "__main__":
    unittest.main()