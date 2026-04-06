from datetime import datetime
from app.services.track_items_service import get_stats, get_stats_on_restaurants
import pytest
from fastapi import HTTPException

mock_orders = [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        },{
        "order_id": "order456",
        "customer_id": "cust789",
        "restaurant_id": 789,
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
        "restaurant_id": 789,
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
    result = get_stats(mock_orders, "restaurant_id")

    assert result[0]["restaurant_id"] == 789
    assert result[0]["count"] == 3

def test_get_stats_invalid(): 
    """Tests the function raises and error with an invalid restaurant id"""
    with pytest.raises(HTTPException):
        get_stats(mock_orders, "restaurant_id_dne")

mock_empty_orders = [{}]

def test_get_stats_none(): 
     """Tests the function raises an error when the orders data is empty"""
     with pytest.raises(HTTPException):
        get_stats(mock_empty_orders, "restaurant_id")


def test_get_stats_on_restaurants_valid(): 
    """Tests the functions returns the right restaurant id and counts it the correct amount of times"""
    result = get_stats(mock_orders, "restaurant_id")

    assert result[0]["restaurant_id"] == 789
    assert result[0]["count"] == 3

