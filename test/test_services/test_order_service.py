import pytest
from fastapi import HTTPException
from datetime import datetime
from app.schemas.OrderStatus import OrderStatus
from app.services.order_service import cancel_order_restaurant_service,accept_order_service,process_order_service

def test_process_order_service_success(mocker):
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = "456"
            self.delivery_address_id = "addr1"
            self.cart_items = [Mock_TempCartItem(1, 1, 4.00),                 
            ]
    class Mock_TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item 
    
    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    process_order_service("cart123")
    
    mock_payment.assert_called_once()
    mock_create_order.assert_called_once()

def test_process_order_service_empty_cart(mocker):
    """checks that method raises 400 exception if a cart has no items in it"""
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = "456"
            self.delivery_address_id = "addr1"
            self.cart_items = []

    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    with pytest.raises(HTTPException) as testException: process_order_service("cart123")
    assert testException.value.status_code ==400

    mock_payment.assert_not_called()
    mock_create_order.assert_not_called()


def test_process_order_service_multiple_items(mocker):
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = "456"
            self.delivery_address_id = "addr1"
            self.cart_items = [Mock_TempCartItem(1, 1, 4.00),
                            Mock_TempCartItem(2, 2, 5.50),                 
            ]
    class Mock_TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item 
    
    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    process_order_service("cart123")
    
    mock_payment.assert_called_once()
    mock_create_order.assert_called_once()

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
                    "created_date": datetime(2026, 2, 20, 12, 34, 56),
                    "delivery_address_id": "addr202"
        }]
    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders", mock_save_orders)
    mocker.patch("app.services.order_service.process_refund_service", return_value = True)
    mocker.patch("app.services.order_service.notify_payment_status", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    result = cancel_order_restaurant_service("order123")
    assert result.order_id == ("order123")
    
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
                    "created_date": datetime(2026, 2, 20, 12, 34, 56),
                    "delivery_address_id": "addr202"
        }]
    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders", mock_save_orders)
    mocker.patch("app.services.order_service.process_refund_service", return_value = True)
    mocker.patch("app.services.order_service.notify_payment_status", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
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
    mocker.patch("app.services.order_service.notify_payment_status", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    
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
    mocker.patch("app.services.order_service.notify_payment_status", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
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
    mocker.patch("app.services.order_service.notify_payment_status", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
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
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
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
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
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
