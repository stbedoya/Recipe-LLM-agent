import unittest
from src.llm.output_validator import RecipeValidator


class TestRecipeValidator(unittest.TestCase):
    def setUp(self):
        self.available_ingredients = [
            {"name": "flour", "quantity": 500, "unit": "g"},
            {"name": "sugar", "quantity": 200, "unit": "g"},
            {"name": "butter", "quantity": 100, "unit": "g"},
        ]
        self.disliked_ingredients = ["egg"]
        self.min_ingredients_required = 2

        self.recipe_validator = RecipeValidator(
            self.available_ingredients,
            self.disliked_ingredients,
            self.min_ingredients_required,
        )

    def test_recipe_validator_initialization(self):
        self.assertEqual(
            self.recipe_validator.available_ingredients,
            self.available_ingredients,
        )
        self.assertEqual(
            self.recipe_validator.disliked_ingredients,
            self.disliked_ingredients,
        )
        self.assertEqual(
            self.recipe_validator.min_ingredients_required,
            self.min_ingredients_required,
        )

    def test_invalid_disliked_ingredients(self):
        with self.assertRaises(ValueError):
            RecipeValidator(self.available_ingredients, "egg")

    def test_invalid_min_ingredients_required(self):
        with self.assertRaises(ValueError):
            RecipeValidator(
                self.available_ingredients, self.disliked_ingredients, 0
            )

        with self.assertRaises(ValueError):
            RecipeValidator(
                self.available_ingredients, self.disliked_ingredients, -1
            )

    def test_validate_recipe_structure_valid(self):
        recipe = {
            "name": "Cake",
            "ingredients": [{"name": "flour", "quantity": 100, "unit": "g"}],
            "steps": ["Mix ingredients"],
            "cooking_time": "30 minutes",
            "difficulty_level": "easy",
        }
        result = self.recipe_validator.validate_recipe_structure(recipe)
        self.assertTrue(result)

    def test_validate_recipe_structure_invalid(self):
        recipe = {
            "name": "Cake",
            "ingredients": [{"name": "flour", "quantity": 100, "unit": "g"}],
            "steps": ["Mix ingredients"],
            "cooking_time": "30 minutes",
        }
        result = self.recipe_validator.validate_recipe_structure(recipe)
        self.assertFalse(result)

    def test_validate_ingredient_quantities_valid(self):
        ingredients = [{"name": "flour", "quantity": 100, "unit": "g"}]
        result = self.recipe_validator.validate_ingredient_quantities(
            ingredients
        )
        self.assertTrue(result)

    def test_validate_ingredient_quantities_invalid(self):
        ingredients = [{"name": "flour", "quantity": 1000, "unit": "g"}]
        result = self.recipe_validator.validate_ingredient_quantities(
            ingredients
        )
        self.assertFalse(result)

    def test_validate_culinary_sense_valid(self):
        ingredients = [
            {"name": "flour", "quantity": 100, "unit": "g"},
            {"name": "butter", "quantity": 100, "unit": "g"},
        ]
        steps = ["Mix flour with butter and bake"]
        result = self.recipe_validator.validate_culinary_sense(
            ingredients, steps
        )
        self.assertTrue(result)

    def test_validate_culinary_sense_invalid_not_enough_ingredients(self):
        ingredients = [{"name": "flour", "quantity": 100, "unit": "g"}]
        steps = ["Mix flour with water"]
        validator = RecipeValidator(
            self.available_ingredients, self.disliked_ingredients, 2
        )
        result = validator.validate_culinary_sense(ingredients, steps)
        self.assertFalse(result)

    def test_validate_culinary_sense_invalid_missing_ingredient_in_steps(self):
        ingredients = [{"name": "flour", "quantity": 100, "unit": "g"}]
        steps = ["Mix water with sugar"]
        result = self.recipe_validator.validate_culinary_sense(
            ingredients, steps
        )
        self.assertFalse(result)

    def test_validate_recipes_valid(self):
        recipes = {
            "recipe_1": {
                "name": "Cake",
                "ingredients": [
                    {"name": "flour", "quantity": 100, "unit": "g"},
                    {"name": "butter", "quantity": 100, "unit": "g"},
                ],
                "steps": ["Mix flour with butter and bake"],
                "cooking_time": "30 minutes",
                "difficulty_level": "easy",
            }
        }
        valid_recipes = self.recipe_validator.validate_recipes(recipes)
        self.assertEqual(len(valid_recipes), 1)

    def test_validate_recipes_invalid(self):
        recipes = {
            "recipe_1": {
                "name": "Cake",
                "ingredients": [
                    {"name": "flour", "quantity": 100, "unit": "g"}
                ],
                "steps": ["Mix water with sugar"],
                "cooking_time": "30 minutes",
                "difficulty_level": "easy",
            }
        }
        valid_recipes = self.recipe_validator.validate_recipes(recipes)
        self.assertEqual(len(valid_recipes), 0)


if __name__ == "__main__":
    unittest.main()
