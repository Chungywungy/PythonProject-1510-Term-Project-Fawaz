import unittest
import copy
from game.character import apply_class_traits


class TestApplyClassTraits(unittest.TestCase):

    def setUp(self):
        self.class_data = {
            "pathway_1": {
                "name": "Sun",
                "level": {
                    "1": {
                        "traits": {
                            "physical": {
                                "effect": {"strength": 2}
                            },
                            "spiritual": {
                                "effect": {"intellect": 1}
                            }
                        }
                    }
                }
            }
        }

        self.character_base = {
            "character": {
                "class": "Sun",
                "level": 1
            }
        }

    def test_apply_single_trait(self):
        character = copy.deepcopy(self.character_base)

        result = apply_class_traits(character, self.class_data)

        self.assertEqual(result["character"]["trait_bonuses"], {
            "physical": {"strength": 2},
            "spiritual": {"intellect": 1}
        })

    def test_empty_traits(self):
        class_data = {
            "pathway_1": {
                "name": "Sun",
                "level": {
                    "1": {
                        "traits": {}
                    }
                }
            }
        }

        character = copy.deepcopy(self.character_base)

        result = apply_class_traits(character, class_data)

        self.assertEqual(result["character"]["trait_bonuses"], {})

    def test_missing_class_raises_error(self):
        character = copy.deepcopy(self.character_base)
        character["character"]["class"] = "Moon"

        with self.assertRaises(ValueError) as context:
            apply_class_traits(character, self.class_data)

        self.assertIn("No pathway found for class 'Moon'", str(context.exception))

    def test_character_is_mutated(self):
        character = copy.deepcopy(self.character_base)

        apply_class_traits(character, self.class_data)

        self.assertIn("trait_bonuses", character["character"])

    def test_multiple_traits_values(self):
        class_data = copy.deepcopy(self.class_data)
        class_data["pathway_1"]["level"]["1"]["traits"]["bonus"] = {
            "effect": {"constitution": 5}
        }

        character = copy.deepcopy(self.character_base)

        result = apply_class_traits(character, class_data)

        self.assertEqual(
            result["character"]["trait_bonuses"]["bonus"],
            {"constitution": 5}
        )


if __name__ == "__main__":
    unittest.main()