import logging
from typing import Dict, List
from pymongo import MongoClient, errors
from src.schemas.ingredient_schemas import (
    UserPreferences,
    Ingredient,
)

logger = logging.getLogger(__name__)


class IngredientManager:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        """
        Initializes the MongoDB connection for managing user ingredient
        preferences.

        Args:
            uri (str): MongoDB connection URI.
            db_name (str): Database name.
            collection_name (str): Collection name.
        """
        try:
            self.client: MongoClient = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            logger.info(
                "Connected to database: %s, collection: %s",
                db_name,
                collection_name,
            )
            self.collection.create_index("user_id", unique=True)
        except errors.ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while initializing IngredientManager: {e}"
            )
            raise

    def save_preferences(self, preferences: UserPreferences) -> Dict[str, str]:
        """
        Saves or updates a user's ingredient preferences in the database.

        Args:
            preferences (UserIngredientPreferences):
            User ingredient preferences, including user ID and ingredient list.

        Returns:
            Dict[str, str]: A dictionary indicating the operation status
            (inserted/updated) and the user ID.
        """
        try:
            self._validate_preferences(preferences.ingredients)
            preference_data = preferences.model_dump()

            result = self.collection.update_one(
                {"user_id": preference_data["user_id"]},
                {"$set": preference_data},
                upsert=True,
            )

            status = "inserted" if result.upserted_id else "updated"
            logger.info(
                f"User preferences {status} for user_id: {preferences.user_id}"
            )
            return {"status": status, "user_id": preferences.user_id}

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except errors.PyMongoError as e:
            logger.error(
                f"MongoDB error occurred while saving preferences: {e}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error while saving preferences: {e}")
            raise

    def _validate_preferences(self, ingredients: List["Ingredient"]) -> None:
        """
        Ensures that no ingredient has contradictory like/dislike preferences.

        Args:
            ingredients (List[IngredientPreference]):
                A list of ingredient preferences.

        Raises:
            ValueError:
                If an ingredient has conflicting like/dislike preferences.
        """
        seen_ingredients: Dict[str, bool] = {}
        for ingredient in ingredients:
            name = ingredient.name.lower()
            if name in seen_ingredients:
                if seen_ingredients[name] != ingredient.like:
                    raise ValueError(
                        f"Contradictory preference for ingredient: {ingredient.name}"
                    )
            seen_ingredients[name] = ingredient.like

    def get_preferences(self, user_id: str) -> Dict[str, List[str]]:
        """
        Retrieves the user's ingredient preferences from the database.

        Args:
            user_id (str): The user ID.

        Returns:
            Dict[str, List[str]]: A dictionary with 'liked_ingredients' and 'disliked_ingredients'.
        """
        try:
            preferences = self.collection.find_one({"user_id": user_id})
            if preferences:
                liked = [
                    ingredient["name"]
                    for ingredient in preferences.get("liked_ingredients", [])
                ]
                disliked = [
                    ingredient["name"]
                    for ingredient in preferences.get(
                        "disliked_ingredients", []
                    )
                ]
                return {
                    "liked_ingredients": liked,
                    "disliked_ingredients": disliked,
                }
            else:
                logger.info(f"No preferences found for user_id: {user_id}")
                return {"liked_ingredients": [], "disliked_ingredients": []}
        except errors.PyMongoError as e:
            logger.error(
                f"MongoDB error occurred while retrieving preferences: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while retrieving preferences for user_id: {user_id}: {e}"
            )
            raise

    def delete_preferences(self, user_id: str) -> bool:
        """
        Deletes the user's ingredient preferences from the database.

        Args:
            user_id (str): The user ID.

        Returns:
            bool: True if the preferences were deleted, False if not found.
        """
        try:
            result = self.collection.delete_one({"user_id": user_id})
            if result.deleted_count > 0:
                logger.info(f"Preferences deleted for user_id: {user_id}")
                return True
            else:
                logger.warning(
                    f"No preferences found to delete for user_id: {user_id}"
                )
                return False
        except errors.PyMongoError as e:
            logger.error(
                f"MongoDB error occurred while deleting preferences: {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while deleting preferences for user_id: {user_id}: {e}"
            )
            raise
