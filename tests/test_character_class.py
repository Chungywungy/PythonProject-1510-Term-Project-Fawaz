import unittest
from unittest.mock import patch
from game.character import character_class


MOCK_CLASS_DATA = {
    "pathway_1": {"name": "Sun"},
    "pathway_2": {"name": "Twilight Giant"}
}


class TestCharacterClass(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        'Sun',
        'y'
    ])
    @patch('game.character.open_json', return_value=MOCK_CLASS_DATA)
    def test_valid_selection(self, mock_json, mock_input):
        self.assertEqual(character_class("fake.json"), "Sun")

    @patch('builtins.input', side_effect=[
        '',              # empty input
        'Sun',
        'y'
    ])
    @patch('game.character.open_json', return_value=MOCK_CLASS_DATA)
    def test_empty_then_valid(self, mock_json, mock_input):
        self.assertEqual(character_class("fake.json"), "Sun")

    @patch('builtins.input', side_effect=[
        'Mage',          # invalid
        'Twilight Giant',
        'y'
    ])
    @patch('game.character.open_json', return_value=MOCK_CLASS_DATA)
    def test_invalid_then_valid(self, mock_json, mock_input):
        self.assertEqual(character_class("fake.json"), "Twilight Giant")

    @patch('builtins.input', side_effect=[
        'Sun',
        'n',             # reject
        'Twilight Giant',
        'y'
    ])
    @patch('game.character.open_json', return_value=MOCK_CLASS_DATA)
    def test_reselect_after_reject(self, mock_json, mock_input):
        self.assertEqual(character_class("fake.json"), "Twilight Giant")

    @patch('builtins.input', side_effect=[
        'Sun',  # pick class
        'maybe',  # invalid confirm
        'Sun',  # re-pick class (loop restarted)
        'y'  # confirm
    ])
    @patch('game.character.open_json', return_value=MOCK_CLASS_DATA)
    def test_invalid_confirmation(self, mock_json, mock_input):
        self.assertEqual(character_class("fake.json"), "Sun")


if __name__ == '__main__':
    unittest.main()