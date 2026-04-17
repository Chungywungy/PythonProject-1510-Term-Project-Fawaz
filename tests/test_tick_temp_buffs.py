import unittest
from unittest.mock import patch
from io import StringIO
import copy

from game.combat import tick_temp_buffs


class TestTickTempBuffs(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_buff_decreases_turns(self, mock_stdout):
        character = {
            "character": {
                "temp_buffs": {
                    "strength_boost": {
                        "turns_remaining": 2
                    }
                }
            }
        }

        result = tick_temp_buffs(character)

        self.assertEqual(result["character"]["temp_buffs"]["strength_boost"]["turns_remaining"], 1)

    @patch("sys.stdout", new_callable=StringIO)
    def test_buff_expires(self, mock_stdout):
        character = {
            "character": {
                "temp_buffs": {
                    "strength_boost": {
                        "turns_remaining": 1
                    }
                }
            }
        }

        result = tick_temp_buffs(character)

        self.assertEqual(result["character"]["temp_buffs"], {})
        self.assertIn("worn off", mock_stdout.getvalue())

    def test_no_temp_buffs(self):
        character = {
            "character": {}
        }

        result = tick_temp_buffs(character)

        self.assertEqual(result["character"].get("temp_buffs", {}), {})

    def test_multiple_buffs_mixed(self):
        character = {
            "character": {
                "temp_buffs": {
                    "a": {"turns_remaining": 1},
                    "b": {"turns_remaining": 3}
                }
            }
        }

        with patch("sys.stdout", new_callable=StringIO):
            result = tick_temp_buffs(character)

        self.assertNotIn("a", result["character"]["temp_buffs"])
        self.assertIn("b", result["character"]["temp_buffs"])
        self.assertEqual(result["character"]["temp_buffs"]["b"]["turns_remaining"], 2)


if __name__ == "__main__":
    unittest.main()