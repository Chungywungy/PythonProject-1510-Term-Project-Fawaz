import unittest
from unittest.mock import patch
import copy

from game.character import level_up


class TestLevelUp(unittest.TestCase):

    def setUp(self):
        self.character = {
            "character": {
                "level": 1,
                "class": "Sun",
                "derived_stats": {
                    "max_health": {"multiplier": 10},
                    "max_mana": {"multiplier": 5}
                },
                "current": {
                    "health": 50,
                    "mana": 20
                }
            }
        }

        self.class_data = {
            "pathway_1": {
                "name": "Sun",
                "level": {
                    "2": {"name": "Light Bearer"}
                }
            }
        }

        self.items_data = {}

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    def test_level_increases(self, mock_traits, mock_stats, mock_print):
        character = copy.deepcopy(self.character)

        mock_traits.side_effect = lambda c, d: c
        mock_stats.return_value = {"constitution": 10, "intellect": 5}

        result = level_up(character, self.class_data, self.items_data)

        self.assertEqual(result["character"]["level"], 2)

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    def test_health_and_mana_recalculated(self, mock_traits, mock_stats, mock_print):
        character = copy.deepcopy(self.character)

        mock_traits.side_effect = lambda c, d: c
        mock_stats.return_value = {"constitution": 12, "intellect": 6}

        result = level_up(character, self.class_data, self.items_data)

        # HP = 12 * 10 = 120
        # Mana = 6 * 5 = 30
        self.assertEqual(result["character"]["current"]["health"], 120)
        self.assertEqual(result["character"]["current"]["mana"], 30)

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    def test_calls_dependencies(self, mock_traits, mock_stats, mock_print):
        character = copy.deepcopy(self.character)

        mock_traits.side_effect = lambda c, d: c
        mock_stats.return_value = {"constitution": 1, "intellect": 1}

        level_up(character, self.class_data, self.items_data)

        mock_traits.assert_called_once()
        mock_stats.assert_called_once()

    @patch('builtins.print')
    @patch('game.character.get_effective_stats')
    @patch('game.character.apply_class_traits')
    def test_class_name_lookup_used(self, mock_traits, mock_stats, mock_print):
        character = copy.deepcopy(self.character)

        mock_traits.side_effect = lambda c, d: c
        mock_stats.return_value = {"constitution": 1, "intellect": 1}

        result = level_up(character, self.class_data, self.items_data)

        # ensures pathway lookup worked (name pulled from level data)
        self.assertIn("Light Bearer", mock_print.call_args_list[1][0][0])


if __name__ == "__main__":
    unittest.main()