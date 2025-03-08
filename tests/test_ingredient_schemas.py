import unittest
from pydantic import ValidationError
from src.schemas.ingredient_schemas import (
    Ingredient,
    AvailableIngredient,
    UserPreferences,
)


class TestUserModels(unittest.TestCase):
    def setUp(self):
        self.valid_ingredient = {"name": "Tomato", "like": True}
        self.valid_available_ingredient = {
            "name": "Flour",
            "quantity": "2",
            "unit": "kg",
        }
        self.valid_user_preferences = {
            "user_id": "user_123",
            "client_name": "John Doe",
            "ingredients": [self.valid_ingredient],
            "available_ingredients": [self.valid_available_ingredient],
        }

    def test_valid_ingredient(self):
        ingredient = Ingredient(**self.valid_ingredient)
        self.assertEqual(ingredient.name, "Tomato")
        self.assertTrue(ingredient.like)

    def test_invalid_ingredient_missing_name(self):
        invalid_data = self.valid_ingredient.copy()
        del invalid_data["name"]
        with self.assertRaises(ValidationError) as context:
            Ingredient(**invalid_data)
        self.assertIn("Field required", str(context.exception))

    def test_valid_available_ingredient(self):
        available_ingredient = AvailableIngredient(
            **self.valid_available_ingredient
        )
        self.assertEqual(available_ingredient.name, "Flour")
        self.assertEqual(available_ingredient.quantity, "2")
        self.assertEqual(available_ingredient.unit, "kg")

    def test_invalid_available_ingredient_missing_quantity(self):
        invalid_data = self.valid_available_ingredient.copy()
        del invalid_data["quantity"]
        with self.assertRaises(ValidationError) as context:
            AvailableIngredient(**invalid_data)
        self.assertIn("Field required", str(context.exception))

    def test_valid_user_preferences(self):
        preferences = UserPreferences(**self.valid_user_preferences)
        self.assertEqual(preferences.user_id, "user_123")
        self.assertEqual(preferences.client_name, "John Doe")
        self.assertEqual(len(preferences.ingredients), 1)
        self.assertEqual(len(preferences.available_ingredients), 1)

    def test_invalid_user_preferences_missing_user_id(self):
        invalid_data = self.valid_user_preferences.copy()
        del invalid_data["user_id"]
        with self.assertRaises(ValidationError) as context:
            UserPreferences(**invalid_data)
        self.assertIn("Field required", str(context.exception))


if __name__ == "__main__":
    unittest.main()
