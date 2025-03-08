from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient (e.g., 'tomato')")
    like: bool = Field(..., description="User's preference for this ingredient (True if liked, False if disliked)")

class AvailableIngredient(BaseModel):
    name: str = Field(..., description="Name of the available ingredient (e.g., 'flour')")
    quantity: str = Field(..., description="Quantity of the ingredient (e.g., '2', '1.5')")
    unit: Optional[str] = Field(None, description="Unit of measurement for the ingredient (e.g., 'kg', 'cups')")

class UserPreferences(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    client_name: str = Field(..., description="Name of the client")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients that the user likes/dislikes")
    available_ingredients: List[AvailableIngredient] = Field(..., description="List of available ingredients along with their quantities and units")

