import unittest

from game.combat import tick_cooldowns


class TestTickCooldowns(unittest.TestCase):

    def test_normal_cooldowns_reduce(self):
        cooldowns = {
            "strike": 3,
            "heal": 1
        }

        result = tick_cooldowns(cooldowns)

        self.assertEqual(result, {
            "strike": 2
        })  # heal should be removed

    def test_all_cooldowns_expire(self):
        cooldowns = {
            "strike": 1,
            "heal": 1
        }

        result = tick_cooldowns(cooldowns)

        self.assertEqual(result, {})

    def test_no_cooldowns(self):
        cooldowns = {}

        result = tick_cooldowns(cooldowns)

        self.assertEqual(result, {})

    def test_does_not_modify_original(self):
        cooldowns = {
            "strike": 2
        }

        original = cooldowns.copy()
        tick_cooldowns(cooldowns)

        self.assertEqual(cooldowns, original)


if __name__ == "__main__":
    unittest.main()