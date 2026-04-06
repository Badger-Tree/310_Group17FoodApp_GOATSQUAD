from datetime import datetime
from app.services.track_items_service import get_stats, get_stats_on_restaurants
import pytest
from fastapi import HTTPException

mock_orders = [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 1,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        },{
        "order_id": "order456",
        "customer_id": "cust789",
        "restaurant_id": 1,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "COMPLETED",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        },
        {
        "order_id": "order789",
        "customer_id": "cust456",
        "restaurant_id": 1,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "COMPLETED",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        }
            ]

def test_get_stats_valid(): 
    """Tests the function returns the correct data for valid inputs"""
    def fake_load_restaurants():
        return [{"restaurant_id": 1, "restaurant_name": "Dominos"}]

    import app.services.track_items_service as service
    service.load_restaurant_name = fake_load_restaurants
   
    result = get_stats(mock_orders, "restaurant_id")

    assert result[0]["restaurant_name"] == "Dominos"
    assert result[0]["order_count"] == 3

def test_get_stats_invalid():
    """Tests the function raises an error with an invalid restaurant id"""
    import pytest
    from fastapi import HTTPException
    import app.services.track_items_service as service

    def fake_load_restaurants():
        return [{"restaurant_id": 1, "restaurant_name": "Dominos"}]

    service.load_restaurant_name = fake_load_restaurants
    mock_orders = [{"order_id": 1, "restaurant_id": 999}]

    with pytest.raises(HTTPException) as httpE:
        service.get_stats(mock_orders, "restaurant_id")


def test_get_stats_on_restaurants_valid(): 
    """Tests the functions returns the right restaurant id and counts it the correct amount of times"""
    result = get_stats(mock_orders, "restaurant_id")

    def fake_load_restaurants():
        return [{"restaurant_id": 1, "restaurant_name": "Dominos"}]

    import app.services.track_items_service as service
    service.load_restaurant_name = fake_load_restaurants
    
    assert result[0]["restaurant_name"] == "Dominos"
    assert result[0]["order_count"] == 3

