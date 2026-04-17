import unittest

from game.character import is_alive


class TestIsAlive(unittest.TestCase):

    def test_alive_character(self):
        character = {
            "character": {
                "current": {
                    "health": 10
                }
            }
        }

        self.assertTrue(is_alive(character))

    def test_dead_character(self):
        character = {
            "character": {
                "current": {
                    "health": 0
                }
            }
        }

        self.assertFalse(is_alive(character))

    def test_negative_health(self):
        character = {
            "character": {
                "current": {
                    "health": -5
                }
            }
        }

        self.assertFalse(is_alive(character))

    def test_missing_current_key(self):
        character = {
            "character": {}
        }

        with self.assertRaises(ValueError) as context:
            is_alive(character)

        self.assertIn("current health", str(context.exception))

    def test_missing_character_key(self):
        character = {}

        with self.assertRaises(ValueError) as context:
            is_alive(character)

        self.assertIn("current health", str(context.exception))


if __name__ == "__main__":
    unittest.main()