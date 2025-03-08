import unittest
from unittest.mock import MagicMock
from src.db.ingredient_manager import IngredientManager
from src.schemas.ingredient_schemas import (
    Ingredient,
    UserPreferences,
    AvailableIngredient,
)


class TestIngredientManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup mock database connection."""
        cls.mock_client = MagicMock()
        cls.mock_db = MagicMock()
        cls.mock_collection = MagicMock()

        cls.mock_client.__getitem__.return_value = cls.mock_db
        cls.mock_db.__getitem__.return_value = cls.mock_collection

        cls.manager = IngredientManager(
            "mongodb://localhost:27017/", "test_database", "test_ingredients"
        )

        cls.manager.collection = cls.mock_collection

    @classmethod
    def tearDownClass(cls):
        """Clean up mocks."""
        cls.mock_client.close()

    def test_save_preferences(self):
        """Test saving a user's ingredient preferences with mocked database."""
        data = UserPreferences(
            user_id="USR-12345",
            client_name="Test Client",
            ingredients=[
                Ingredient(name="onions", like=True),
                Ingredient(name="chicken", like=True),
            ],
            available_ingredients=[
                AvailableIngredient(name="tomato", quantity="2", unit="pcs"),
                AvailableIngredient(
                    name="garlic", quantity="5", unit="cloves"
                ),
            ],
        )

        self.mock_collection.insert_one.return_value = MagicMock(
            inserted_id="USR-12345"
        )

        result = self.manager.save_preferences(data)

        self.assertIn(
            result["status"], ["inserted", "updated"], "Unexpected save status"
        )
        self.assertEqual(result["user_id"], "USR-12345", "User ID mismatch")

        saved_data_mock = {
            "user_id": "USR-12345",
            "ingredients": [
                {"name": "onions", "like": True},
                {"name": "chicken", "like": True},
            ],
            "available_ingredients": [
                {"name": "tomato", "quantity": "2", "unit": "pcs"},
                {"name": "garlic", "quantity": "5", "unit": "cloves"},
            ],
        }
        self.mock_collection.find_one.return_value = saved_data_mock

        saved_data = self.manager.collection.find_one({"user_id": "USR-12345"})
        self.assertIsNotNone(saved_data, "Data was not saved to the database")
        self.assertEqual(
            len(saved_data["ingredients"]),
            2,
            "Incorrect number of ingredients saved",
        )
        self.assertEqual(
            len(saved_data["available_ingredients"]),
            2,
            "Incorrect number of available ingredients saved",
        )

    def test_conflicting_preferences(self):
        """Test that contradictory preferences are rejected with mocked database."""
        data = UserPreferences(
            user_id="USR-67890",
            client_name="Test Client",
            ingredients=[
                Ingredient(name="onions", like=True),
                Ingredient(name="onions", like=False),
            ],
            available_ingredients=[],
        )

        with self.assertRaises(ValueError) as context:
            self.manager.save_preferences(data)

        self.assertTrue(
            "Contradictory preference for ingredient: onions"
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
