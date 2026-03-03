from fastapi import APIRouter, status, HTTPException
from typing import List
from ..schemas.food_item import FoodItem, FoodItemCreate, FoodItemUpdate
from ..services.food_item_service import (list_food_items, create_food_item, get_food_by_id, update_food_item, delete_food_item)

router = APIRouter(prefix="/food-items", tags=["food"])

@router.get("", response_model=List[FoodItem], summary="List all food items")
def get_all_food():
    return list_food_items()

@router.post("", response_model=FoodItem, summary="Create a new food item", status_code=status.HTTP_201_CREATED)
def post_food(payload: FoodItemCreate):
    return create_food_item(payload)

@router.get("/{food_id}", response_model=FoodItem, summary="Get a single food item")
def get_food(food_id: int):
    item = get_food_by_id(food_id)
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    return item

@router.put("/{food_id}", response_model=FoodItem, summary="Update an existing food item")
def put_food(food_id: int, payload: FoodItemUpdate):
    return update_food_item(food_id, payload)

@router.delete("/{food_id}", summary="Delete an existing food item", status_code=status.HTTP_204_NO_CONTENT)
def remove_food(food_id: int):
    delete_food_item(food_id)
    return None