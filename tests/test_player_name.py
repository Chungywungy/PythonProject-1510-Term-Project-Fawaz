import unittest
from unittest.mock import patch
from game.character import player_name


class TestPlayerName(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '',        # empty input
        'alex',    # re-enter name
        'y'        # confirm
    ])
    def test_empty_then_valid_name(self, mock_input):
        self.assertEqual(player_name(), 'Alex')

    @patch('builtins.input', side_effect=[
        'john',    # initial name
        'y'        # confirm
    ])
    def test_accept_valid_name(self, mock_input):
        self.assertEqual(player_name(), 'John')

    @patch('builtins.input', side_effect=[
        'john',    # initial name
        'n',       # reject
        'mike',    # new name
        'y'        # confirm
    ])
    def test_reenter_after_reject(self, mock_input):
        self.assertEqual(player_name(), 'Mike')

    @patch('builtins.input', side_effect=[
        'john',    # initial name
        'maybe',   # invalid confirm
        'y'        # valid confirm
    ])
    def test_invalid_confirmation_then_valid(self, mock_input):
        self.assertEqual(player_name(), 'John')

    @patch('builtins.input', side_effect=[
        '',        # empty
        '',        # empty again
        'sam',     # valid name
        'y'        # confirm
    ])
    def test_multiple_empty_inputs(self, mock_input):
        self.assertEqual(player_name(), 'Sam')


if __name__ == '__main__':
    unittest.main()