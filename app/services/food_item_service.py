from typing import List, Optional
from fastapi import HTTPException
from decimal import Decimal
from ..schemas.food_item import FoodItem, FoodItemCreate, FoodItemUpdate, FoodItemBase
from ..repositories.food_item_repo import load_all, save_all

def list_food_items() -> List[FoodItem]:
    #unpacking list of dictionaries from load_all() with **it into objs
    return [FoodItem(**it) for it in load_all()]

def create_food_item(payload: FoodItemCreate) -> FoodItem:
    items = load_all()

    #generate new ids by finding curr highest id + 1; if empty list, start @ 1 
    new_id = max([it.get("food_item_id", 0) for it in items], default=0) + 1

    #create new obj using data from payload + new id
    new_food = FoodItem(
        food_item_id = new_id,
        food_name = payload.food_name.strip(),
        restaurant_id = payload.restaurant_id,
        price = payload.price,
        description = payload.description.strip() if payload.description else None,
        course = payload.course.strip() 
    )

    #convert pydantic model to dict to save in db
    items.append(new_food.model_dump())
    save_all(items)
    return new_food

def get_food_by_id(food_id: int) -> FoodItem:
    items = load_all()
    for it in items:
        if it.get("food_item_id") == food_id:
            return FoodItem(**it)
    raise HTTPException(status_code=404, detail=f"Food item {food_id} not found")

def update_food_item(food_id: int, payload: FoodItemUpdate) -> FoodItem:
    items = load_all()
    for idx, it in enumerate(items):
        if it.get("food_item_id") == food_id:
            update_data = it.copy()
            update_data.update(payload.model_dump(exclude_unset=True))

            updated_item = FoodItem(**update_data)
            items[idx] = updated_item.model_dump()
            save_all(items)
            return updated_item
    raise HTTPException(status_code=404, detail=f"Food item {food_id} not found")

def delete_food_item(food_id: int) -> None:
    items = load_all()
    #create new list that doesnt include item to be deleted
    filtered_items = [it for it in items if it.get("food_item_id") != food_id]

    #checking length; if it's the same, nothing was deletted
    if len(filtered_items) == len(items):
        raise HTTPException(status_code=404, detail=f"Food item {food_id} not found")
    
    save_all(filtered_items)