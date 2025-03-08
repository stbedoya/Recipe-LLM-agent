from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.schemas.recipes_schemas import RecipeCollection


RECIPE_PARSER = JsonOutputParser(pydantic_object=RecipeCollection)

RECIPE_PROMPT = PromptTemplate(
    template=(
        "Generate 5 structured recipes based on the following available ingredients: {available_ingredients}. "
        "Ensure the recipes include liked ingredients {liked_ingredients} "
        "and avoid using disliked ingredients {disliked_ingredients}. "
        "Each recipe should include the following fields: name, ingredients, steps, cooking time, and difficulty level. "
        "{format_instructions}"
    ),
    input_variables=[
        "available_ingredients",
        "liked_ingredients",
        "disliked_ingredients",
    ],
    partial_variables={
        "format_instructions": RECIPE_PARSER.get_format_instructions()
    },
)
