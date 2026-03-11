from decimal import Decimal
import os
from pathlib import Path
from app.repositories import food_item_repo
from app.schemas.food_item import FoodItem

def test_save_and_load_repository():
    """Test that saving and loading food items works correctly."""
    original_path = food_item_repo.DATA_PATH
    test_csv = Path("app/data/test_food_items.csv")
    food_item_repo.DATA_PATH = test_csv

    try:
        item_obj = FoodItem(
            food_item_id=999, 
            restaurant_id=999, 
            food_name="Burger", 
            price=9.99, 
            description="A delicious burger", 
            course="Main"
            )
    
        test_items = [item_obj.model_dump()]

        food_item_repo.save_all(test_items)
        loaded_items = food_item_repo.load_all()

        assert len(loaded_items) > 0
        assert loaded_items[0]["food_item_id"] == 999
        assert loaded_items[0]["food_name"] == "Burger"
        assert loaded_items[0]["price"] == Decimal("9.99")
        assert loaded_items[0]["description"] == "A delicious burger"
        assert loaded_items[0]["course"] == "Main"

    finally:
        if test_csv.exists():
            os.remove(test_csv)
        food_item_repo.DATA_PATH = original_path