import pytest
from fastapi import HTTPException
from datetime import datetime
from app.schemas.OrderStatus import OrderStatus
from app.services.order_service import get_order_by_order_id_service, get_orders_by_restaurant_service, get_orders_by_userid_service

def test_get_order_by_order_id_service_success(mocker):
    """tests that get_order_by_order_id_service() will successfully get an order given valid order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_order_by_order_id_service("order123")
    
    assert result.order_id == "order123"
    assert result.restaurant_id == "rest789"
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")
    assert result.items[0].food_item_id ==1
    assert result.items[1].food_item_id ==2

def test_get_order_by_order_id_service_order_not_found(mocker):
    """tests that get_order_by_order_id_service() will return empty object if order id not found"""

    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
    }]
        
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_order_by_order_id_service("order1")
    assert result is None
    
def test_get_orders_by_restaurant_service_success(mocker):
    """tests that get_orders_by_restaurant_service() will successfully get an order given valid restaurant id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_orders_by_restaurant_service("rest789")
    assert len(result) == 1
    assert result[0].order_id=="order123"
    assert len(result[0].items) == 2
    assert result[0].items[0].food_item_id ==1
    assert result[0].items[1].food_item_id ==2
    
def test_get_orders_by_restaurant_service_not_found(mocker):
    """tests that get_orders_by_restaurant_service() will will return empty object if restaurant id not found"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    result = get_orders_by_restaurant_service("666")
    assert result == []
    
def test_get_orders_by_userid_service_success(mocker):
    """tests that get_orders_by_userid_service() will successfully get an order given valid user id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_orders_by_userid_service("cust456")
    assert len(result) == 1
    assert result[0].order_id=="order123"
    assert len(result[0].items) == 2
    
def test_get_orders_by_userid_service_not_found(mocker):
    """tests that get_orders_by_userid_service() will generate error if userid not found"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    result = get_orders_by_userid_service("616")
    assert result == []
    