"Data schemas for Recipes"

from typing import List, Dict
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    """Represents a structured recipe."""

    name: str = Field(..., description="Name of the recipe")
    ingredients: List[Dict[str, str]] = Field(
        ...,
        description="List of ingredients with their quantities (name and quantity)",
    )
    steps: List[str] = Field(
        ..., description="Step-by-step cooking instructions"
    )
    cooking_time: str = Field(..., description="Total cooking time")
    difficulty_level: str = Field(
        ..., description="Difficulty level of the recipe"
    )


class RecipeCollection(BaseModel):
    """Encapsulates multiple recipes, each with a unique key."""

    recipes: Dict[str, Recipe] = Field(
        ..., description="A dictionary mapping recipe keys to Recipe objects"
    )


class UserRequest(BaseModel):
    user_id: str
