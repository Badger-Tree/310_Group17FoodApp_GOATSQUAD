from app.repositories import track_food_items_repo_csv
from app.schemas.track_food_items_schema import TrackFoodResponse
from pathlib import Path
import os

def test_save_and_load_repository_track_food_itemd_repo():
    """Test that saving and loading food items works correctly."""
    original_path = track_food_items_repo_csv.DATA_PATH
    test_csv = Path("app/data/test_items_repo.csv")
    track_food_items_repo_csv.DATA_PATH = test_csv

    try:
        item_obj = TrackFoodResponse(
            food_item_id= 3, 
            order_count = 1
            )
    
        test_items = [item_obj.model_dump()]

        track_food_items_repo_csv.save_all(test_items)
        loaded_items = track_food_items_repo_csv.load_all()

        assert len(loaded_items) > 0
        assert loaded_items[0]["food_item_id"] == 3
        assert loaded_items[0]["order_count"] == 1

    finally:
        if test_csv.exists():
            os.remove(test_csv)
        track_food_items_repo_csv.DATA_PATH = original_path