import unittest
import json
import os

from game import  file_tampering


class TestOpenJson(unittest.TestCase):

    def setUp(self):
        # Create test files
        with open("valid.json", "w") as f:
            json.dump({"key": "value"}, f)

        with open("empty.json", "w") as f:
            f.write("")

        with open("invalid.json", "w") as f:
            f.write("{invalid json}")

        with open("not_json.txt", "w") as f:
            f.write("Just text")

    def tearDown(self):
        for file in ["valid.json", "empty.json", "invalid.json", "not_json.txt"]:
            if os.path.exists(file):
                os.remove(file)

    def test_valid_json(self):
        result = file_tampering.open_json("valid.json")
        self.assertEqual(result, {"key": "value"})

    def test_wrong_extension(self):
        with self.assertRaises(ValueError) as context:
            file_tampering.open_json("not_json.txt")
        self.assertEqual(str(context.exception), "File is not a JSON file.")

    def test_empty_json(self):
        with self.assertRaises(ValueError) as context:
            file_tampering.open_json("empty.json")
        self.assertEqual(str(context.exception), "The JSON file is empty.")

    def test_invalid_json(self):
        with self.assertRaises(ValueError) as context:
            file_tampering.open_json("invalid.json")
        self.assertEqual(str(context.exception), "The JSON file is empty.")


if __name__ == "__main__":
    unittest.main()