from app.repositories import track_items_repo_csv
from app.schemas.track_items_schema import TrackRestaurantResponse
from pathlib import Path
import os

def test_save_and_load_repository_restaurant():
    """Test that saving and loading items works correctly."""
    original_path = track_items_repo_csv.DATA_PATH
    test_csv = Path("app/data/test_items_repo.csv")
    track_items_repo_csv.DATA_PATH = test_csv

    try:
        item_obj = TrackRestaurantResponse(
            restaurant_id= 999, 
            count = 1
            )
    
        test_items = [item_obj.model_dump()]

        track_items_repo_csv.save_all(test_items)
        loaded_items = track_items_repo_csv.load_all()

        assert len(loaded_items) > 0
        assert loaded_items[0]["restaurant_id"] == 999
        assert loaded_items[0]["count"] == 1

    finally:
        if test_csv.exists():
            os.remove(test_csv)
        track_items_repo_csv.DATA_PATH = original_path