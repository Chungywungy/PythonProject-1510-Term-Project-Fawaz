import unittest
from unittest.mock import patch
from game.character import character_name
from game.file_tampering import open_json


class TestCharacterName(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '',      # initial name (empty)
        'y'      # accept default
    ])
    def test_accept_default_name(self, mock_input):
        self.assertEqual(character_name(), 'Amon')

    @patch('builtins.input', side_effect=[
        '',      # initial name (empty)
        'n',     # reject default
        'alex',  # new name
        'y'      # confirm
    ])
    def test_reenter_name_after_rejecting_default(self, mock_input):
        self.assertEqual(character_name(), 'Alex')

    @patch('builtins.input', side_effect=[
        'john',  # initial name
        'y'      # confirm
    ])
    def test_accept_valid_name(self, mock_input):
        self.assertEqual(character_name(), 'John')

    @patch('builtins.input', side_effect=[
        'john',  # initial name
        'n',     # reject
        'mike',  # new name
        'y'      # confirm
    ])
    def test_change_name_after_rejecting(self, mock_input):
        self.assertEqual(character_name(), 'Mike')

    @patch('builtins.input', side_effect=[
        'john',  # initial name
        'maybe', # invalid confirmation
        'y'      # valid confirmation
    ])
    def test_invalid_confirmation_input(self, mock_input):
        self.assertEqual(character_name(), 'John')


if __name__ == '__main__':
    unittest.main()