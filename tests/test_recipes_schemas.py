import unittest
from pydantic import ValidationError
from src.schemas.recipes_schemas import Recipe, RecipeCollection, UserRequest


class TestRecipeModels(unittest.TestCase):
    def setUp(self):
        self.valid_recipe_data = {
            "name": "Pasta Carbonara",
            "ingredients": [
                {"name": "Spaghetti", "quantity": "200g"},
                {"name": "Eggs", "quantity": "2"},
                {"name": "Pancetta", "quantity": "100g"},
                {"name": "Parmesan", "quantity": "50g"},
            ],
            "steps": [
                "Boil water and cook spaghetti.",
                "Fry pancetta until crispy.",
                "Mix eggs and cheese together.",
                "Combine everything and serve.",
            ],
            "cooking_time": "30 minutes",
            "difficulty_level": "Medium",
        }
        self.valid_recipe_collection = {
            "recipes": {"carbonara": self.valid_recipe_data}
        }

    def test_valid_recipe(self):
        recipe = Recipe(**self.valid_recipe_data)
        self.assertEqual(recipe.name, "Pasta Carbonara")
        self.assertEqual(len(recipe.ingredients), 4)
        self.assertEqual(len(recipe.steps), 4)
        self.assertIsInstance(recipe.cooking_time, str)
        self.assertIsInstance(recipe.difficulty_level, str)

    def test_invalid_recipe_missing_fields(self):
        invalid_data = self.valid_recipe_data.copy()
        del invalid_data["name"]
        with self.assertRaises(ValidationError) as context:
            Recipe(**invalid_data)
        self.assertIn("Field required", str(context.exception))

    def test_invalid_recipe_wrong_type(self):
        invalid_data = self.valid_recipe_data.copy()
        invalid_data["cooking_time"] = 30
        with self.assertRaises(ValidationError) as context:
            Recipe(**invalid_data)
        self.assertIn("Input should be a valid string", str(context.exception))

    def test_valid_recipe_collection(self):
        collection = RecipeCollection(**self.valid_recipe_collection)
        self.assertEqual(len(collection.recipes), 1)
        self.assertIn("carbonara", collection.recipes)
        self.assertIsInstance(collection.recipes["carbonara"], Recipe)

    def test_invalid_recipe_collection_wrong_type(self):
        invalid_collection = {"recipes": [self.valid_recipe_data]}
        with self.assertRaises(ValidationError) as context:
            RecipeCollection(**invalid_collection)
        self.assertIn(
            "Input should be a valid dictionary", str(context.exception)
        )

    def test_valid_user_request(self):
        request = UserRequest(user_id="12345")
        self.assertEqual(request.user_id, "12345")

    def test_invalid_user_request_missing_user_id(self):
        with self.assertRaises(ValidationError) as context:
            UserRequest()
        self.assertIn("Field required", str(context.exception))


if __name__ == "__main__":
    unittest.main()
