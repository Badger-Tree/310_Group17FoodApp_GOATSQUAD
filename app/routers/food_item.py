from fastapi import APIRouter, status, HTTPException
from typing import List
from ..schemas.food_item import FoodItem, FoodItemCreate, FoodItemUpdate
from ..services.food_item_service import (create_food_item, get_food_by_id, update_food_item, delete_food_item, filter_food_items)

router = APIRouter(prefix="/food-items", tags=["food"])

@router.get("", response_model=List[FoodItem], summary="List and filter food items")
def get_all_food(name: str = None, restaurant_id: int = None, course: str = None):
    """GET all food items, with optional filtering by name, restaurant_id and course. Returns list of food items that match criteria. If no filters, returns all food items."""
    return filter_food_items(name, restaurant_id, course)

@router.post("", response_model=FoodItem, summary="Create a new food item", status_code=status.HTTP_201_CREATED)
def post_food(payload: FoodItemCreate):
    """Creates a new food item with the provided data and returns the created item."""
    return create_food_item(payload)

@router.get("/{food_id}", response_model=FoodItem, summary="Get a single food item")
def get_food(food_id: int):
    """Gets a single food item by its ID and if not found, raises 404 error."""
    item = get_food_by_id(food_id)
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    return item

@router.put("/{food_id}", response_model=FoodItem, summary="Update an existing food item")
def put_food(food_id: int, payload: FoodItemUpdate):
    """Updates an existing food item with the provided data and only fields with values will be updated; if item not found, raises 404 error."""
    return update_food_item(food_id, payload)

@router.delete("/{food_id}", summary="Delete an existing food item", status_code=status.HTTP_204_NO_CONTENT)
def remove_food(food_id: int):
    """Deletes a food item by its ID and if not found, raises 404 error. Returns no content when successful."""
    success = delete_food_item(food_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with ID {food_id} not found"
            )
    return None