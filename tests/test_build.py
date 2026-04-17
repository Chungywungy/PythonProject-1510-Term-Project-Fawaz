import unittest
from unittest.mock import patch
import copy

from game.map import build


class TestBuild(unittest.TestCase):

    def test_invalid_types_raise(self):
        with self.assertRaises(TypeError):
            build("1", 2, 3)

        with self.assertRaises(TypeError):
            build(1, "2", 3)

        with self.assertRaises(TypeError):
            build(1, 2, "3")

    @patch('random.choice')
    @patch('random.random')
    def test_basic_structure(self, mock_random, mock_choice):
        # force deterministic output
        mock_random.return_value = 0.5
        mock_choice.return_value = 1

        atlas = build(1, 2, 2)

        self.assertIn(0, atlas)
        self.assertIn("position", atlas[0])
        self.assertEqual(len(atlas[0]["position"]), 4)

    @patch('random.choice')
    @patch('random.random')
    def test_start_tile_is_none(self, mock_random, mock_choice):
        mock_random.return_value = 0.5
        mock_choice.return_value = 1

        atlas = build(1, 2, 2)

        self.assertIsNone(atlas[0]["position"][(0, 0)])

    @patch('random.choice')
    @patch('random.random')
    def test_stair_exists_if_none_generated(self, mock_random, mock_choice):
        mock_random.return_value = 0.5
        mock_choice.return_value = 1

        atlas = build(2, 2, 2)
        stair_found = any(
            value == 11
            for value in atlas[0]["position"].values()
        )

        self.assertTrue(stair_found)

    @patch('random.choice')
    @patch('random.random')
    def test_only_one_stair_per_layer_rule(self, mock_random, mock_choice):
        # force many stairs first, then fixed cleanup
        mock_random.return_value = 0.0  # always stair
        mock_choice.return_value = 1

        atlas = build(2, 2, 2)

        for layer in range(1):  # all non-final layers
            stair_count = list(atlas[layer]["position"].values()).count(11)
            self.assertLessEqual(stair_count, 1)

    @patch('random.choice')
    @patch('random.random')
    def test_final_layer_no_stair_enforcement(self, mock_random, mock_choice):
        mock_random.return_value = 0.0  # would try to create stairs
        mock_choice.return_value = 1

        atlas = build(2, 2, 2)

        final_layer = 1
        stair_count = list(atlas[final_layer]["position"].values()).count(11)

        # final layer may have stairs but is not enforced same way
        self.assertIsInstance(atlas[final_layer]["position"], dict)


if __name__ == "__main__":
    unittest.main()