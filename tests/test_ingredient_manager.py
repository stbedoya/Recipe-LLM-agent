import unittest
from pymongo import MongoClient
from src.db.ingredient_manager import IngredientManager
from src.schemas.ingredient_schemas import (
    Ingredient,
    UserPreferences,
    AvailableIngredient,
)


class TestIngredientManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup a test database connection once for the class."""
        cls.client = MongoClient("mongodb://localhost:27017/")
        cls.db = cls.client["test_database"]
        cls.collection = cls.db["test_ingredients"]
        cls.collection.drop()
        cls.manager = IngredientManager(
            "mongodb://localhost:27017/", "test_database", "test_ingredients"
        )

    @classmethod
    def tearDownClass(cls):
        """Cleanup: Drop the test collection after tests run."""
        cls.db.drop_collection("test_ingredients")
        cls.client.close()

    def test_save_preferences(self):
        """Test saving a user's ingredient preferences."""
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

        result = self.manager.save_preferences(data)

        self.assertIn(
            result["status"], ["inserted", "updated"], "Unexpected save status"
        )
        self.assertEqual(result["user_id"], "USR-12345", "User ID mismatch")

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
        """Test that contradictory preferences are rejected."""
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
