import pytest 
from pydantic import ValidationError
from app.schemas.track_food_items_schema import TrackFoodBase, TrackFoodResponse

def test_track_food_item_base_valid(): 
    """Tests TrackFoodBase with valid data returns what it is supposed to"""
    data = { 
        "food_item_id": 2,
        "order_count": 3
    }

    schema = TrackFoodBase(**data)

    assert schema.food_item_id == 2
    assert schema.order_count == 3


def test_track_food_item_base_negative(): 
    """Tests TrackFoodBase with negative data raises an error"""
    data = { 
        "food_item_id": -1,
        "order_count": 3
    }
   
    with pytest.raises(ValidationError):
         TrackFoodBase(**data)



def test_track_food_item_base_none(): 
    """Tests TrackFoodBase with none value raises an error"""
    data = { 
        "food_item_id": 22,
        "order_count": None
    }
   
    with pytest.raises(ValidationError):
         TrackFoodBase(**data)

def test_track_food_item_response_valid(): 
    """Tests TrackFoodResponse with valid data returns what its supposed to"""
    data = { 
        "food_item_id": 1,
        "order_count": 3
    }

    schema = TrackFoodResponse(**data)

    assert schema.food_item_id == 1
    assert schema.order_count == 3