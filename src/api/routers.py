import uvicorn
import logging
from config import settings

from src.schemas.recipes_schemas import UserRequest
from src.llm.recipe_generator import RecipeGenerator
from src.llm.prompts import RECIPE_PROMPT, RECIPE_PARSER
from src.llm.output_validator import RecipeValidator
from src.llm.openai_llm import OpenAILLM
from src.db.mongodb_handler import MongoDBHandler
from src.schemas.ingredient_schemas import UserPreferences
from fastapi import FastAPI, HTTPException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

mongo_handler = MongoDBHandler(
    uri=settings.MONGODB_URI,
    db_name=settings.MONGODB_NAME,
    collection_name=settings.MONGODB_COLLECTION_NAME,
)


@app.post("/insert_user_preferences/")
async def insert_user_preferences(preferences: UserPreferences):
    """
    Insert user preferences data into MongoDB.

    Args:
        preferences (UserPreferences): The user preferences to insert.

    Returns:
        dict: A message indicating whether the insertion was successful.
    """
    logger.info(
        f"Inserting user preferences for user_id: {preferences.user_id}..."
    )

    try:
        inserted_id = await mongo_handler.insert_data(preferences.model_dump())
        logger.info(f"Data inserted with ID: {inserted_id}")
        return {"message": f"User preferences inserted with ID: {inserted_id}"}

    except Exception as e:
        logger.error(f"Error inserting user preferences: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert user preferences: {str(e)}",
        )


@app.post("/get_user_preferences/")
async def get_user_preferences(request: UserRequest):
    """
    Retrieve user preferences from MongoDB by user ID.
    """
    user_id = request.user_id
    logger.info(f"Fetching user preferences for user_id: {user_id}...")

    try:
        preferences = await mongo_handler.fetch_data({"user_id": user_id})

        if preferences:
            logger.info(f"Preferences found for user_id {user_id}")
            return {"preferences": preferences[0]}
        else:
            logger.warning(f"No preferences found for user_id {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"No preferences found for user_id: {user_id}",
            )

    except Exception as e:
        logger.error(
            f"Error retrieving preferences for user_id {user_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve user preferences: {str(e)}",
        )


@app.post("/generate_recipes/")
async def generate_recipes_for_user(request: UserRequest):
    """
    Retrieve user data from MongoDB asynchronously and generate recipes.
    """
    user_id = request.user_id
    logger.info(f"Fetching preferences for user_id: {user_id}...")

    try:
        user_data = await mongo_handler.fetch_data({"user_id": user_id})

        if not user_data:
            logger.warning(f"No data found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="User data not found.")

        user_preferences = user_data[0]
        ingredients = user_preferences.get("ingredients", [])
        available_ingredients = user_preferences.get(
            "available_ingredients", []
        )
        liked_ingredients = [ing["name"] for ing in ingredients if ing["like"]]
        disliked_ingredients = [
            ing["name"] for ing in ingredients if not ing["like"]
        ]

        llm = OpenAILLM(
            model_name="gpt-4", api_key=settings.OPENAI_API_KEY, temperature=0
        )
        recipe_generator = RecipeGenerator(llm, RECIPE_PARSER, RECIPE_PROMPT)

        available_ingredients_list = [
            f"{ing['name']} ({ing['quantity']})"
            for ing in available_ingredients
        ]

        inputs = {
            "available_ingredients": available_ingredients_list,
            "liked_ingredients": liked_ingredients,
            "disliked_ingredients": disliked_ingredients,
        }

        logger.info("Generating recipes based on user preferences...")
        output = await recipe_generator.generate_recipes(
            inputs["available_ingredients"],
            inputs["liked_ingredients"],
            inputs["disliked_ingredients"],
        )
        logger.info(f"Recipes generated: {output}")
        logger.info(f"Type recipes generated: {type(output)}")

        recipe_validator = RecipeValidator(
            disliked_ingredients=disliked_ingredients,
            available_ingredients=available_ingredients,
            min_ingredients_required=3,
        )
        valid_recipes = recipe_validator.validate_recipes(output["recipes"])

        if valid_recipes:
            logger.info(f"Generated {len(valid_recipes)} valid recipes.")
            for idx, recipe in enumerate(valid_recipes, start=1):
                logger.info(f"Recipe {idx}: {recipe}")
        else:
            logger.warning("No valid recipes were generated.")

        if valid_recipes:
            logger.info(f"Generated {len(valid_recipes)} valid recipes.")
            return {"recipes": valid_recipes}
        else:
            logger.warning("No valid recipes were generated.")
            return {"message": "No valid recipes found."}

    except Exception as e:
        logger.error(f"Error generating recipes: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Recipe generation failed: {str(e)}"
        )


@app.on_event("shutdown")
def shutdown_db():
    """Close MongoDB connection on shutdown."""
    mongo_handler.close_connection()
    logger.info("MongoDB connection closed.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
