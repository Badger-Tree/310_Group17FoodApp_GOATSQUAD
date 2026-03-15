import pytest
from fastapi import HTTPException
from datetime import datetime
from app.schemas.Order import OrderCreate
from app.schemas.OrderStatus import OrderStatus
from app.services.order_service import cancel_order_restaurant_service,accept_order_service


def test_cancel_order_restaurant_service_success(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
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
    mocker.patch("app.services.order_service.process_refund_service", return_value = True)
    result = cancel_order_restaurant_service("order123")
    assert result.order_id == ("order123")
    
    
def test_cancel_order_restaurant_service_refund_failed(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
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
    mocker.patch("app.services.order_service.process_refund_service", return_value = False)
    
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order123")
    assert testException.value.status_code ==400
    
def test_cancel_order_restaurant_service_order_not_found(mocker):
    """tests that cancel_order_customer_service() will generate an error if order is not found by order id"""
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

    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order1")
    assert testException.value.status_code ==404

def test_cancel_order_restaurant_service_completed(mocker):
    """tests that cancel_order_customer_service() will generate an error if order has already been completed"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "COMPLETED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order123")
    assert testException.value.status_code ==400

def test_accept_order_service_success(mocker):
    """tests that accept_order_service() will successfully accept an order given valid order id from restaurant side"""
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
    result = accept_order_service("order123")
    assert result.status == OrderStatus.APPROVED   
    
def test_accept_order_service_order_not_found(mocker):
    """tests that accept_order_service() will generate an error if order is not found by order id"""
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
    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404

def test_accept_order_service_accepted(mocker):
    """tests that accept_order_service() will generate an error if order has already been accepted"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "IN_PREPARATION",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404