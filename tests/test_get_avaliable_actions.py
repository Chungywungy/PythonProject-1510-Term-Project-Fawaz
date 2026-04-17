import unittest

from game.combat import get_available_actions


class TestGetAvailableActions(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "class": "Sun",
                "level": 1
            }
        }

        self.class_data = {
            "pathway_1": {
                "name": "Sun",
                "level": {
                    "1": {
                        "actions": {
                            "strike": {"name": "Strike"},
                            "heal": {"name": "Heal"},
                            "buff": {"name": "Buff"}
                        }
                    }
                }
            }
        }

        self.cooldowns = {
            "strike": 0,
            "heal": 2,
            "buff": 0
        }

    def test_filters_cooldowns_correctly(self):
        result = get_available_actions(self.character, self.class_data, self.cooldowns)

        # only strike and buff should be available
        self.assertIn("strike", result)
        self.assertIn("buff", result)
        self.assertNotIn("heal", result)

    def test_all_actions_available_when_no_cooldowns(self):
        cooldowns = {}

        result = get_available_actions(self.character, self.class_data, cooldowns)

        self.assertEqual(set(result.keys()), {"strike", "heal", "buff"})

    def test_invalid_class_raises_error(self):
        bad_character = {
            "character": {
                "class": "Unknown",
                "level": 1
            }
        }

        with self.assertRaises(ValueError):
            get_available_actions(bad_character, self.class_data, self.cooldowns)


if __name__ == "__main__":
    unittest.main()