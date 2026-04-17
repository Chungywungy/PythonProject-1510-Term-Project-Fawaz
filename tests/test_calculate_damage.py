import unittest

from game.combat import calculate_damage


class TestCalculateDamage(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "base_stats": {
                    "strength": 10,
                    "dexterity": 5
                },
                "temp_buffs": {
                    "attack_boost": {
                        "amount": 3
                    }
                }
            }
        }

    def test_single_stat_scaling(self):
        action = {
            "scaling": {
                "stat": "strength",
                "multiplier": 2
            }
        }

        result = calculate_damage(self.character, action)

        # 10 * 2 + 3 buff = 23
        self.assertEqual(result, 23)

    def test_multi_stat_scaling(self):
        character = {
            "character": {
                "base_stats": {
                    "strength": 10,
                    "dexterity": 5
                },
                "temp_buffs": {}
            }
        }

        action = {
            "scaling": [
                {"stat": "strength", "multiplier": 1},
                {"stat": "dexterity", "multiplier": 2}
            ]
        }

        result = calculate_damage(character, action)

        # (10*1) + (5*2) = 20
        self.assertEqual(result, 20)

    def test_no_buff_applied(self):
        character = {
            "character": {
                "base_stats": {
                    "strength": 10
                }
            }
        }

        action = {
            "scaling": {
                "stat": "strength",
                "multiplier": 3
            }
        }

        result = calculate_damage(character, action)

        self.assertEqual(result, 30)

    def test_missing_temp_buffs(self):
        character = {
            "character": {
                "base_stats": {
                    "strength": 4
                }
            }
        }

        action = {
            "scaling": {
                "stat": "strength",
                "multiplier": 2
            }
        }

        result = calculate_damage(character, action)

        self.assertEqual(result, 8)


if __name__ == "__main__":
    unittest.main()