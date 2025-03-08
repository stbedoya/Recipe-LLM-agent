import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecipeValidator:
    def __init__(
        self,
        available_ingredients: List[Dict[str, Any]],
        disliked_ingredients: List[str] = [],
        min_ingredients_required: int = 1,
    ):
        """
        The RecipeValidator is a mechanism for validating LLM output and ensure recipe quality.

        Args:
            available_ingredients (list): List of available ingredients with their quantities.
            disliked_ingredients (list): List of disliked ingredients (optional).
            min_ingredients_required (int): Minimum number of ingredients required for a recipe to be valid.
        """
        if not available_ingredients or not isinstance(
            available_ingredients, list
        ):
            raise ValueError("available_ingredients must be a non-empty list.")

        if not all(
            isinstance(ingredient, dict)
            and "name" in ingredient
            and "quantity" in ingredient
            for ingredient in available_ingredients
        ):
            raise ValueError(
                "Each ingredient must be a dictionary with 'name', 'quantity' and 'unit'."
            )

        if disliked_ingredients and not isinstance(disliked_ingredients, list):
            raise ValueError("disliked_ingredients must be a list.")

        if (
            not isinstance(min_ingredients_required, int)
            or min_ingredients_required <= 0
        ):
            raise ValueError(
                "min_ingredients_required must be a positive integer."
            )

        self.available_ingredients = available_ingredients
        self.disliked_ingredients = disliked_ingredients
        self.min_ingredients_required = min_ingredients_required

    def validate_recipe_structure(self, recipe: Dict[str, Any]) -> bool:
        """
        Validates that a recipe contains all necessary fields.

        Args:
            recipe (dict): The recipe data.

        Returns:
            bool: True if the recipe structure is valid, False otherwise.
        """
        required_fields = [
            "name",
            "ingredients",
            "steps",
            "cooking_time",
            "difficulty_level",
        ]
        for field in required_fields:
            if field not in recipe:
                logger.error(f"Recipe is missing required field: {field}")
                return False
        return True

    def validate_ingredient_quantities(
        self, ingredients: List[Dict[str, int]]
    ) -> bool:
        """
        Validates that the ingredients in the recipe have available quantities.

        Args:
            ingredients (list): List of ingredients in the recipe with their required quantities.

        Returns:
            bool: True if all ingredients are available in the required quantities, False otherwise.
        """
        for ingredient in ingredients:
            ingredient_name = ingredient["name"]
            required_quantity = ingredient["quantity"]

            available_ingredient = next(
                (
                    item
                    for item in self.available_ingredients
                    if item["name"] == ingredient_name
                ),
                None,
            )
            if not available_ingredient:
                continue

            available_quantity = available_ingredient["quantity"]

            if not self.is_quantity_sufficient(
                required_quantity, available_quantity
            ):
                logger.error(
                    f"Ingredient '{ingredient_name}' has insufficient quantity. Required: {required_quantity}, Available: {available_quantity}"
                )
                return False

        return True

    def is_quantity_sufficient(
        self, required_quantity: int, available_quantity: int
    ) -> bool:
        """
        Helper function to check if the available quantity is sufficient.

        Args:
            required_quantity (int): The required quantity.
            available_quantity (int): The available quantity.

        Returns:
            bool: True if available quantity is sufficient, False otherwise.
        """
        if required_quantity <= available_quantity:
            return True
        else:
            return False

    def validate_culinary_sense(
        self, ingredients: List[Dict[str, str]], steps: List[str]
    ) -> bool:
        """
        Ensures the recipe makes culinary sense: checks if ingredients are mentioned in steps
        and if there are enough ingredients.

        Args:
            ingredients (list): Ingredients listed in the recipe.
            steps (list): Steps listed in the recipe.

        Returns:
            bool: True if the recipe makes culinary sense, False otherwise.
        """
        if len(ingredients) < self.min_ingredients_required:
            logger.error(
                f"Recipe contains fewer than {self.min_ingredients_required} ingredients."
            )
            return False

        for ingredient in ingredients:
            if not any(
                ingredient["name"].lower() in step.lower() for step in steps
            ):
                logger.error(
                    f"Ingredient '{ingredient['name']}' is not mentioned in the steps."
                )
                return False

        return True

    def validate_recipes(
        self, recipes: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validates a list of recipes. Each recipe is checked for structure, ingredients, and culinary sense.

        Args:
            recipes (dict): A dictionary of recipe data, where the key is 'recipe_1', 'recipe_2', etc.

        Returns:
            list: Valid recipes.
        """
        valid_recipes = []
        for recipe_key, recipe in recipes.items():
            if not self.validate_recipe_structure(recipe):
                logger.error(f"Recipe {recipe_key} structure is invalid.")
                continue

            if not self.validate_ingredient_quantities(recipe["ingredients"]):
                logger.error(
                    f"Recipe {recipe_key} contains unavailable ingredients."
                )
                continue

            if not self.validate_culinary_sense(
                recipe["ingredients"], recipe["steps"]
            ):
                logger.error(
                    f"Recipe {recipe_key} does not make culinary sense."
                )
                continue
            valid_recipes.append(recipe)

        return valid_recipes
