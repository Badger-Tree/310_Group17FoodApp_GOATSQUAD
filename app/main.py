from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from random import randint
from typing import Any

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

data = [
    {
       "food_item_id": 1,
       "restaurant_id": 1,
       "food_name": "Cheese Pizza",
       "price": 9.99,
       "description": "Pizza with mozzarella cheese and tomato sauce",
       "is_available": True,
       "created_at": "2024-06-01T12:00:00Z",
       "category_id": 1
    }
]

"""
food_items
- food_item_id: int
- restaurant_id: int (foreign key to restaurants)
- food_name: str
- price: float
- description: str
- is_available: bool
- created_at: datetime
- category_id: int (foreign key to categories)
"""

@app.get("/food_items")
async def get_food_items():
    return {"food_item": data}

@app.get("/food_items/{food_item_id}")
async def get_food_item(food_item_id: int):
    for food_item in data:
        if food_item.get("food_item_id") == food_item_id:
            return {"food_item": food_item}
        raise HTTPException(status_code=404, detail="Food item not found")
    
@app.post("/food_items")
async def create_food_item(body: dict[str, Any]):
    
    new : Any = {
        "food_item_id": randint(2, 100),
        "restaurant_id": 1,
        "food_name": body.get("food_name"),
        "price": 7.99,
        "description": "Burger with a plant-based patty, lettuce, tomato, and vegan mayo",
        "is_available": True,
        "created_at": datetime.now(),
        "category_id": 2
    }

    data.append(new)
    return {"food_item": new}