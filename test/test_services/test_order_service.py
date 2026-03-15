import pytest
from fastapi import HTTPException
from datetime import datetime
from app.schemas.Order import OrderCreate
from app.schemas.OrderStatus import OrderStatus
from app.services.order_service import cancel_order_restaurant_service,accept_order_service,process_order_service

def test_process_order_service(mocker):
    
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




# def test_create_order_service_success(monkeypatch):
#     """tests that create_order_service() will successfully create an order given valid input"""
#     def mock_load_orders():
#         return [{}]
#     def mock_load_order_items():
#         return []
#     def mock_save_all_orders(orders):
#         return orders
#     def mock_save_all_order_items(order_items):
#         return order_items
  
#     class Mock_TempCart:
#         def __init__(self):
#             self.cart_id = "cart123"
#             self.customer_id = "123"
#             self.restaurant_id = "456"
#             self.delivery_address_id = "addr1"
#             self.cart_items = [Mock_TempCartItem(1, 1, 4.00),
#                             Mock_TempCartItem(2, 2, 5.50),                 
#             ]
#     class Mock_TempCartItem:
#         def __init__(self, food_item_id, quantity, price_per_item):
#             self.food_item_id = food_item_id
#             self.quantity = quantity
#             self.price_per_item = price_per_item 
#     monkeypatch.setattr("app.services.order_service.load_orders", mock_load_orders)
#     monkeypatch.setattr("app.services.order_service.load_order_items", mock_load_order_items)
#     monkeypatch.setattr("app.services.order_service.save_all_orders", mock_save_all_orders)
#     monkeypatch.setattr("app.services.order_service.save_all_order_items", mock_save_all_order_items)
#     monkeypatch.setattr("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    
#     input_data = OrderCreate(
#                 restaurant_id="456",
#                 customer_id="123",
#                 cart_id="cart789",
#                 delivery_address_id="addr1",
#                 items=[]
#             )

#     result = create_order_service(input_data)
#     assert result.customer_id == "123"
#     assert result.restaurant_id== "456"
#     assert result.delivery_address_id =="addr1"
#     assert len(result.items) == 2
#     assert result.items[0].food_item_id == 1
    
# def test_create_order_service_empty_cart(monkeypatch):
#     """tests that create_order_service() will generate error given empty cart"""

#     def mock_load_orders():
#         return []
#     def mock_load_order_items():
#         return []
#     def mock_save_all_orders(orders):
#         return orders
#     def mock_save_all_order_items(order_items):
#         return order_items
  
#     class Mock_TempCart:
#         def __init__(self):
#             self.cart_id = "cart123"
#             self.customer_id = "123"
#             self.restaurant_id = "456"
#             self.delivery_address_id = "addr1"
#             self.cart_items = []
#     class Mock_TempCartItem:
#         def __init__(self, food_item_id, quantity, price_per_item):
#             self.food_item_id = food_item_id
#             self.quantity = quantity
#             self.price_per_item = price_per_item 
    
#     monkeypatch.setattr("app.services.order_service.load_orders", mock_load_orders)
#     monkeypatch.setattr("app.services.order_service.load_order_items", mock_load_order_items)
#     monkeypatch.setattr("app.services.order_service.save_all_orders", mock_save_all_orders)
#     monkeypatch.setattr("app.services.order_service.save_all_order_items", mock_save_all_order_items)
#     monkeypatch.setattr("app.services.order_service.temp_get_restaurant_fee", lambda restaurant_id: 1.0)
#     monkeypatch.setattr("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    
#     input_data = OrderCreate(
#                 restaurant_id="456",
#                 customer_id="123",
#                 cart_id="cart789",
#                 delivery_address_id="addr1",
#                 items=[]
#             )
#     with pytest.raises(HTTPException) as testException: create_order_service(input_data)
#     assert testException.value.status_code ==400
# def test_create_order_service_subtotal_multiple_items(monkeypatch):
#     """tests that create_order_service() will successfully generate a total given multiple order items"""
#     def mock_load_orders():
#         return [{}]
#     def mock_load_order_items():
#         return []
#     def mock_save_all_orders(orders):
#         return orders
#     def mock_save_all_order_items(order_items):
#         return order_items

#     class Mock_TempCart:
#         def __init__(self):
#             self.cart_id = "cart123"
#             self.customer_id = "123"
#             self.restaurant_id = "456"
#             self.delivery_address_id = "addr1"
#             self.cart_items = [Mock_TempCartItem(1, 1, 4.00),
#                             Mock_TempCartItem(2, 2, 5.50),                 
#             ]
#     class Mock_TempCartItem:
#         def __init__(self, food_item_id, quantity, price_per_item):
#             self.food_item_id = food_item_id
#             self.quantity = quantity
#             self.price_per_item = price_per_item 
#     monkeypatch.setattr("app.services.order_service.load_orders", mock_load_orders)
#     monkeypatch.setattr("app.services.order_service.load_order_items", mock_load_order_items)
#     monkeypatch.setattr("app.services.order_service.save_all_orders", mock_save_all_orders)
#     monkeypatch.setattr("app.services.order_service.save_all_order_items", mock_save_all_order_items)
#     monkeypatch.setattr("app.services.order_service.get_cart_by_id", lambda cart_id: Mock_TempCart())
    
#     input_data = OrderCreate(
#                 restaurant_id="456",
#                 customer_id="123",
#                 cart_id="cart789",
#                 delivery_address_id="addr1",
#                 items=[]
#             )

#     result = create_order_service(input_data)
#     assert result.total_amount == 4.00+5.5+5.5+1




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
