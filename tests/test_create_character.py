import unittest
from unittest.mock import patch, MagicMock
import copy
from game.character import create_character


class TestCreateCharacter(unittest.TestCase):

    def setUp(self):
        self.mock_character_template = {
            "character": {
                "name": "",
                "player": "",
                "class": "",
                "level": 0,
                "xp": 0,
                "trait_bonuses": {},
                "derived_stats": {
                    "max_health": {"multiplier": 10},
                    "max_mana": {"multiplier": 5}
                },
                "current": {
                    "health": 0,
                    "mana": 0
                }
            }
        }

        self.class_data = {}
        self.items_data = {}

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    @patch('game.character.open_json')
    def test_create_character_basic(
        self,
        mock_open,
        mock_apply_traits,
        mock_get_stats,
        mock_print
    ):
        mock_open.return_value = copy.deepcopy(self.mock_character_template)

        # after trait application
        mock_apply_traits.side_effect = lambda c, d: c

        # fake stats
        mock_get_stats.return_value = {
            "constitution": 10,
            "intellect": 5
        }

        result = create_character(
            character="Amon",
            player="Player1",
            file="fake.json",
            pathway="Sun",
            class_data=self.class_data,
            items_data=self.items_data
        )

        self.assertEqual(result["character"]["name"], "Amon")
        self.assertEqual(result["character"]["player"], "Player1")
        self.assertEqual(result["character"]["class"], "Sun")
        self.assertEqual(result["character"]["level"], 1)
        self.assertEqual(result["character"]["xp"], 0)

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    @patch('game.character.open_json')
    def test_health_and_mana_calculation(
        self,
        mock_open,
        mock_apply_traits,
        mock_get_stats,
        mock_print
    ):
        mock_open.return_value = copy.deepcopy(self.mock_character_template)

        mock_apply_traits.side_effect = lambda c, d: c

        mock_get_stats.return_value = {
            "constitution": 10,
            "intellect": 5
        }

        result = create_character(
            "Amon",
            "Player1",
            "fake.json",
            "Sun",
            self.class_data,
            self.items_data
        )

        # derived stats:
        # health = 10 * 10 = 100
        # mana = 5 * 5 = 25
        self.assertEqual(result["character"]["current"]["health"], 100)
        self.assertEqual(result["character"]["current"]["mana"], 25)

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    @patch('game.character.open_json')
    def test_function_calls_chain(
        self,
        mock_open,
        mock_apply_traits,
        mock_get_stats,
        mock_print
    ):
        mock_open.return_value = copy.deepcopy(self.mock_character_template)
        mock_apply_traits.side_effect = lambda c, d: c
        mock_get_stats.return_value = {
            "constitution": 1,
            "intellect": 1
        }

        create_character(
            "Amon",
            "Player1",
            "fake.json",
            "Sun",
            self.class_data,
            self.items_data
        )

        mock_apply_traits.assert_called_once()
        mock_get_stats.assert_called_once()


if __name__ == "__main__":
    unittest.main()