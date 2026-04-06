import pytest 
from pydantic import ValidationError
from app.schemas.track_items_schema import TrackRestaurantBase, TrackRestaurantResponse

def test_track_restaurant_base_valid(): 
    """Tests TrackRestaurantBase with valid data returns what it is supposed to"""
    data = { 
        "restaurant_id": 789,
        "count": 3
    }

    schema = TrackRestaurantBase(**data)

    assert schema.restaurant_id == 789
    assert schema.count == 3


def test_track_restaurant_base_invalid(): 
    """Tests TrackRestaurantBase with invalid data raises an error"""
    data = { 
        "restaurant_id": "4",
        "quantity": "33"
    }

    with pytest.raises(ValidationError):
         TrackRestaurantBase(**data)


def test_track_restarant_base_negative(): 
    """Tests TrackRestaurantBase with negative data raises an error"""
    data = { 
        "restaurant_id": -1,
        "quantity": 3
    }
   
    with pytest.raises(ValidationError):
         TrackRestaurantBase(**data)



def test_track_restarant_base_none(): 
    """Tests TrackRestaurantBase with none value raises an error"""
    data = { 
        "restaurant_id": 4,
        "quantity": None
    }
   
    with pytest.raises(ValidationError):
         TrackRestaurantBase(**data)

def test_track_restaurant_response_valid(): 
    """Tests TrackRestaurantResponse with valid data returns what its supposed to"""
    data = { 
        "restaurant_id": 789,
        "count": 3
    }

    schema = TrackRestaurantResponse(**data)

    assert schema.restaurant_id == 789
    assert schema.count == 3