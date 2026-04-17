import unittest
from unittest.mock import patch
from io import StringIO

from game.combat import flee


class TestFlee(unittest.TestCase):

    @patch("random.random", return_value=0.8)
    @patch("sys.stdout", new_callable=StringIO)
    def test_flee_success(self, mock_stdout, mock_random):
        character = {
            "character": {
                "name": "Amon"
            }
        }

        result = flee(character)

        self.assertTrue(result)
        self.assertIn("successfully fled", mock_stdout.getvalue().lower())

    @patch("random.random", return_value=0.2)
    @patch("sys.stdout", new_callable=StringIO)
    def test_flee_failure(self, mock_stdout, mock_random):
        character = {
            "character": {
                "name": "Amon"
            }
        }

        result = flee(character)

        self.assertFalse(result)
        self.assertIn("failed to flee", mock_stdout.getvalue().lower())


if __name__ == "__main__":
    unittest.main()