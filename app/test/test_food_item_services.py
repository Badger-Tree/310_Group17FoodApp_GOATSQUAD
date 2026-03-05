from services.food_item_service import create_food_item
from schemas.food_item import FoodItemCreate

def test_create_food_item(): 

    payload = {
        "food_name": "Cheesecake",
        "restaurant_id": 2,
        "price": "7.0",
        "description": "Fluffy original cheesecake",
        "course": "dessert",
        "food_item_id": 4
  }

    result = create_food_item(payload)
    assert result == { 
        "food_name": "foodName",
        "restaurant_id": 30,
        "price": 3.33,
        "description": "description",
        "course": "comp sci",
    }