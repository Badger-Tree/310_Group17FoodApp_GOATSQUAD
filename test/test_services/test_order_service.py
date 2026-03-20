from app.schemas.Address import AddressResponse
import pytest
from fastapi import HTTPException
from datetime import datetime
from app.schemas.OrderStatus import OrderStatus
from app.services.order_service import accept_order_service, cancel_order_customer_service, get_order_by_order_id_service, get_order_status_by_id_service, get_orders_by_restaurant_service, get_orders_by_userid_service,cancel_order_restaurant_service, cancel_order_restaurant_service, accept_order_service, process_order_service, set_order_status_service

mock_address_response = AddressResponse(address_id= "7",
            user_id= "cust456",
            street= "111 Shire Lane",
            city= "Hobbiton",
            postal_code= "H0B 1T5",
            instructions= "leave at driveway",
            created_date = "2025-01-20T11:34:56")

def test_get_order_by_order_id_service_success(mocker):
    """tests that get_order_by_order_id_service() will successfully get an order given valid order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
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
    assert result.restaurant_id == 789
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")
    assert result.items[0].food_item_id ==1
    assert result.items[1].food_item_id ==2

def test_get_order_by_order_id_service_order_not_found(mocker):
    """tests that get_order_by_order_id_service() will return empty object if order id not found"""

    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
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
                    "restaurant_id": 789,
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

    result = get_orders_by_restaurant_service(789)
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
                    "restaurant_id": 789,
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
                    "restaurant_id": 789,
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
                    "restaurant_id": 789,
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

def test_process_order_service_success(mocker):
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = 456
            self.cart_items = [Mock_TempCartItem(1, 1, 4.00),                 
            ]
    class Mock_TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item 
            
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.notify_payment_status")
    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mocker.patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response)
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    result = process_order_service("cart123","7")
    mock_payment.assert_called_once()
    mock_create_order.assert_called_once()

def test_process_order_service_cart_not_found(mocker):
    """checks that method raises 404 exception there is no cart matching input id"""
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = 456
            self.cart_items = []

    mocker.patch("app.services.order_service.get_cart_by_id", side_effect=HTTPException(status_code=404))
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.notify_payment_status")
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    mocker.patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response)
    
    with pytest.raises(HTTPException) as testException: process_order_service("nocart","7")
    assert testException.value.status_code ==404
    mock_payment.assert_not_called()
    mock_create_order.assert_not_called()

def test_process_order_service_empty_cart(mocker):
    """checks that method raises 400 exception if a cart has no items in it"""
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = 456
            self.cart_items = []

    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.notify_payment_status")
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    mocker.patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response)
    
    with pytest.raises(HTTPException) as testException: process_order_service("cart123","7")
    assert testException.value.status_code ==400
    mock_payment.assert_not_called()
    mock_create_order.assert_not_called()

def test_process_order_service_address_not_found(mocker):
    """checks that method raises 404 exception there is no address matching input id"""
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = 456
            self.cart_items = [Mock_TempCartItem(1, 1, 4.00),                 
            ]
    class Mock_TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item 

    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.notify_payment_status")
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    mocker.patch("app.services.order_service.get_address_by_id_service", side_effect=HTTPException(status_code=404))
    
    with pytest.raises(HTTPException) as testException: process_order_service("cart123","nocart")
    assert testException.value.status_code ==404
    mock_payment.assert_not_called()
    mock_create_order.assert_not_called()

def test_process_order_service_multiple_items(mocker):
    class Mock_TempCart:
        def __init__(self):
            self.cart_id = "cart123"
            self.customer_id = "123"
            self.restaurant_id = 456
            self.cart_items = [Mock_TempCartItem(1, 1, 4.00),
                            Mock_TempCartItem(2, 2, 5.50),                 
            ]
    class Mock_TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item 
    
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.notify_payment_status")
    mocker.patch("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    mock_payment = mocker.patch("app.services.order_service.process_payment_service", return_value = True)
    mock_create_order = mocker.patch("app.services.order_service.create_order_service")
    mocker.patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response)
    
    result = process_order_service("cart123","7")
    mock_payment.assert_called_once()
    mock_create_order.assert_called_once()

def test_cancel_order_restaurant_service_success(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
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
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    result = cancel_order_restaurant_service("order123")
    assert result.order_id == ("order123")
    
def test_cancel_order_restaurant_service_refund_failed(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.notify_refund_issued")
    mocker.patch("app.services.order_service.notify_order_status_update")
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels")
    mocker.patch("app.services.order_service.process_refund_service", return_value=False)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order123")
    assert testException.value.status_code ==400
    
def test_cancel_order_restaurant_service_order_not_found(mocker):
    """tests that cancel_order_restaurant_service() will generate an error if order is not found by order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order1")
    assert testException.value.status_code ==404

def test_get_order_status_by_id_service_success(mocker):
    """tests that get_order_status_by_id_service will return an Order status given a valid order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "CANCELED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    
    result = get_order_status_by_id_service("order123")
    assert result == OrderStatus.CANCELED
    
def test_get_order_status_by_id_service_order_not_found(mocker):
    """tests that get_order_status_by_id_service will return a 404 exception if it cannot find the given order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    with pytest.raises(HTTPException) as testException: get_order_status_by_id_service("noorder")
    assert testException.value.status_code ==404
    
def test_set_order_status_service_success(mocker):
    """tests that set_order_status will change the status of an order given a valid order id and status"""

    mock_orders= [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": None,
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": "2026-02-20T12:34:56",
        "delivery_address_id": "addr202"
        }]

    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders", mock_save_orders)
    
    result = set_order_status_service("order123",OrderStatus.APPROVED)
    assert result.status == OrderStatus.APPROVED

def test_set_order_status_service_order_not_found(mocker):
    """tests that set_order_status will raise a 404 error if the order is not found"""

    mock_orders= [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": None,
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": "2026-02-20T12:34:56",
        "delivery_address_id": "addr202"
        }]

    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    with pytest.raises(HTTPException) as testException: set_order_status_service("noorder",OrderStatus.APPROVED)
    assert testException.value.status_code ==404
    
def test_cancel_order_customer_success(mocker):
    """tests that cancel_order_customer_service() will cancel an order given valid input"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": datetime(2026, 2, 20, 12, 34, 56),
                    "delivery_address_id": "addr202"
        }]
    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value=mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels", return_value=None)

    
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    result = cancel_order_customer_service("order123")
    assert result.order_id == ("order123")
    

def test_cancel_order_customer_service_completed(mocker):
    """tests that cancel_order_customer_service() will generate an error if order has already been completed"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "COMPLETED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]


    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels", return_value=None)
    with pytest.raises(HTTPException) as testException: cancel_order_customer_service("order123")
    assert testException.value.status_code ==400

def test_accept_order_service_success(mocker):
    """tests that accept_order_service() will successfully accept an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
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
    assert result.status == OrderStatus.ACCEPTED 
    
def test_accept_order_service_order_not_found(mocker):
    """tests that accept_order_service() will generate an error if order is not found by order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404

def test_accept_order_service_accepted(mocker):
    """tests that accept_order_service() will generate an error if order has already been accepted"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "IN_PREPARATION",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404

