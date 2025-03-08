import logging
from typing import List
from src.schemas.recipes_schemas import Recipe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeGenerator:
    def __init__(self, llm, parser, prompt_template):
        """
        Initializes the RecipeGenerator with LLM, parser, and prompt template.
        
        Args:
            llm (LLM): The LLM interface for generating responses.
            parser (RecipeParser): The parser for converting response text into Recipe objects.
            prompt_template (str): The template for formatting the prompt.
        """
        if not llm:
            raise ValueError("LLM must be provided")
        if not parser:
            raise ValueError("Parser must be provided")
        if not prompt_template:
            raise ValueError("Prompt template must be provided")

        self.llm = llm
        self.parser = parser
        self.prompt_template = prompt_template

    async def generate_recipes(
        self,
        ingredients: List[str],
        liked_ingredients: List[str],
        disliked_ingredients: List[str]
    ) -> List[Recipe]:
        """
        Generates structured recipes based on user preferences.

        Args:
            ingredients (List[str]): List of available ingredients.
            liked_ingredients (List[str]): List of liked ingredients.
            disliked_ingredients (List[str]): List of disliked ingredients.

        Returns:
            List[Recipe]: List of generated recipes.
        """
        self._validate_ingredients(ingredients, liked_ingredients, disliked_ingredients)

        prompt_text = self._format_prompt(ingredients, liked_ingredients, disliked_ingredients)

        try:
            response_text = await self._invoke_llm(prompt_text)
            return await self._parse_recipes(response_text)
        except Exception as e:
            logger.error(f"Error generating recipes: {e}")
            return []

    def _format_prompt(
        self, available_ingredients: List[str], liked_ingredients: List[str], disliked_ingredients: List[str]
    ) -> str:
        """
        Formats the prompt with provided ingredients and preferences.

        Args:
            available_ingredients (List[str]): List of available ingredients.
            liked_ingredients (List[str]): List of liked ingredients.
            disliked_ingredients (List[str]): List of disliked ingredients.

        Returns:
            str: Formatted prompt string.
        """
        return self.prompt_template.format(
            available_ingredients=available_ingredients,
            liked_ingredients=liked_ingredients,
            disliked_ingredients=disliked_ingredients,
            format_instructions=self.parser.get_format_instructions(),
        )

    async def _invoke_llm(self, prompt_text: str) -> str:
        """
        Invokes the LLM and retrieves the response.

        Args:
            prompt_text (str): The formatted prompt text.

        Returns:
            str: The response text from the LLM.
        """
        try:
            response = await self.llm.generate_response(prompt_text)
            return response.content if hasattr(response, "content") else str(response)
        except AttributeError as e:
            logger.error(f"Invalid response from LLM: {e}")
            raise ValueError("LLM response does not have expected 'content' attribute")
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise ValueError("Error invoking LLM")

    async def _parse_recipes(self, response_text: str) -> List[Recipe]:
        """
        Parses the LLM response into a list of Recipe objects.

        Args:
            response_text (str): The raw response text from the LLM.

        Returns:
            List[Recipe]: List of parsed Recipe objects.
        """
        try:
            return self.parser.parse(response_text)
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return []

    def _validate_ingredients(
        self, ingredients: List[str], liked_ingredients: List[str], disliked_ingredients: List[str]
    ) -> None:
        """
        Validates the ingredients input to ensure it's not empty or invalid.

        Args:
            ingredients (List[str]): List of available ingredients.
            liked_ingredients (List[str]): List of liked ingredients.
            disliked_ingredients (List[str]): List of disliked ingredients.

        Raises:
            ValueError: If any of the ingredients lists are invalid.
        """
        if not all(isinstance(ingredient, str) for ingredient in ingredients):
            raise ValueError("All ingredients must be strings")
        if not all(isinstance(ingredient, str) for ingredient in liked_ingredients):
            raise ValueError("All liked ingredients must be strings")
        if not all(isinstance(ingredient, str) for ingredient in disliked_ingredients):
            raise ValueError("All disliked ingredients must be strings")

        if not ingredients:
            logger.warning("No available ingredients provided")
        if not liked_ingredients:
            logger.warning("No liked ingredients provided")
        if not disliked_ingredients:
            logger.warning("No disliked ingredients provided")