import pytest
from fastapi import HTTPException

mock_order_items = [{
    "food_item_id": 1,
    "quantity" : 1,
    "price_per_item" : "1.00",
    "order_item_id" : "1",
    "order_id" : "order123"
    },{
    "food_item_id": 1,
    "quantity" : 1,
    "price_per_item" : "1.00",
    "order_item_id" : "1",
    "order_id" : "order123"
}]

mock_orders= [{
    "order_id": "order123",
    "customer_id": "cust456",
    "restaurant_id": 101,
    "cart_id": "cart101",
    "delivery_id": "delivery",
    "status": "PENDING",
    "total_amount": 26.66,
    "created_date": "2026-02-20T12:34:56",
    "delivery_address_id": "addr202"
    }]

mock_food_item = {
    "food_item_id": 1,
    "restaurant_id": 101,
    "food_name": "Margherita Pizza",
    "price": 12.50,
    "description": "Classic pizza with fresh mozzarella, tomato sauce, and basil",
    "course": "Main"
}

mock_tracked_item = [{
    "food_item_id": 1,
    "food_name": "Margherita Pizza",
    "order_count": 5
}]


def test_get_stats_valid(mocker):
    """Test get_stats_on_food returns correct results for valid restaurant_id"""
    mocker.patch("app.services.track_food_items_service.load_order_items",return_value=mock_order_items)
    mocker.patch("app.services.track_food_items_service.load_orders",return_value=mock_orders)
    mocker.patch("app.services.track_food_items_service.get_food_by_id",return_value=mock_food_item)
    mocker.patch("app.services.track_food_items_service.load_food_items",return_value=mock_tracked_item)
    mocker.patch("app.services.track_food_items_service.save_food_items",return_value=None)

    from app.services.track_food_items_service import get_stats_on_food

    result = get_stats_on_food(101) 

    assert result[0].food_item_id == 1
    assert result[0].food_name == "Margherita Pizza"
    assert result[0].order_count == 2



mock_order_items_invalid = []
mock_orders_invalid = [{"order_id": "order1", "restaurant_id": 101}]
mock_food_item_invalid = []
mock_tracked_item_invalid = []

def test_get_stats_invalid(mocker):
    mocker.patch("app.services.track_food_items_service.load_order_items", return_value=mock_order_items_invalid)
    mocker.patch("app.services.track_food_items_service.load_orders", return_value=mock_orders_invalid)
    mocker.patch("app.services.track_food_items_service.get_food_by_id", return_value=mock_food_item_invalid)
    mocker.patch("app.services.track_food_items_service.load_food_items", return_value=mock_tracked_item_invalid)
    mocker.patch("app.services.track_food_items_service.save_food_items", return_value=None)

    from app.services.track_food_items_service import get_stats_on_food
    with pytest.raises(HTTPException) as exc_info:
            get_stats_on_food(222)


