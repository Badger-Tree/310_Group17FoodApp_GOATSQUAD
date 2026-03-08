# import pytest
# from fastapi import HTTPException
# from datetime import datetime
# from app.schemas.Order import OrderResponse, OrderCreate
# from app.schemas.OrderItem import OrderItemResponse,OrderItemCreate # type: ignore
# from app.schemas.OrderStatus import OrderStatus
# from app.services.order_service import create_order_service, get_order_by_order_id_service, get_orders_by_restaurant_service, get_orders_by_userid_service, get_order_status_by_id_service, cancel_order_customer_service, cancel_order_restaurant_service,accept_order_service 


# def test_create_order_service_success(monkeypatch):
#     """tests that create_order_service() will successfully create an order given valid input"""
#     def mock_load_orders():
#         return [{
#                     "order_id": "order123",
#                     "customer_id": "cust456",
#                     "restaurant_id": "rest789",
#                     "cart_id": "cart101",
#                     "delivery_id": None,
#                     "status": "PENDING",
#                     "total_amount": 42.75,
#                     "created_date": "2026-02-20T12:34:56",
#                     "delivery_address_id": "addr202"
#         }]
#     def mock_load_order_items():
#         return [
#                 {
#                     "order_item_id": "item1",
#                     "order_id": "order1",
#                     "food_item_id": "food1",
#                     "quantity": 2,
#                     "price_per_item": 10.00
#                 },{
#                     "order_item_id": "item2",
#                     "order_id": "order1",
#                     "food_item_id": "food3",
#                     "quantity": 6,
#                     "price_per_item": 1.11
#                 }
#             ]
#     class Mock_TempCart:
#         def __init__(self):
#             self.cart_id = "cart123"
#             self.customer_id = "123"
#             self.restaurant_id = "456"
#             self.delivery_address_id = "1"
#             self.cart_items = [Mock_TempCartItem("food1", 1, 4.00),
#                             Mock_TempCartItem("food2", 5, 1.20),
#                             Mock_TempCartItem("food3", 2, 2.00),                  
#             ]
#     class Mock_TempCartItem:
#         def __init__(self, food_item_id, quantity, price_per_item):
#             self.food_item_id = food_item_id
#             self.quantity = quantity
#             self.price_per_item = price_per_item 
#     monkeypatch.setattr("app.services.order_service.load_orders", mock_load_orders)
#     monkeypatch.setattr("app.services.order_service.load_order_items", mock_load_order_items)
#     monkeypatch.setattr("app.services.order_service.get_restaurant_fee", return_value=1.0)
#     monkeypatch.setattr("app.services.order_service.get_cart_by_id", return_value=Mock_TempCart())
    
#     input_data = OrderCreate(
#                 restaurant_id="456",
#                 customer_id="123",
#                 cart_id="cart789",
#                 delivery_address_id="addr1",
#                 items=[
#                     OrderItemCreate(food_item_id="food1", quantity=1, price_per_item=4.00),
#                     OrderItemCreate(food_item_id="food2", quantity=2, price_per_item=5.50)
#                 ]
#             )
    
    
#     result = create_order_service(**input_data)
    
    
# # def test_create_order_service_empty_cart(monkeypatch):
# """tests that create_order_service() will generate error given empty cart"""
# # def test_create_order_service_duplicate_order_id(monkeypatch):
# """tests that create_order_service() will generate error given a duplicate uuid"""
# # def test_create_order_service_subtotal_multiple_items(monkeypatch):
# """tests that create_order_service() will successfully generate a total given multiple order items"""


# # def test_get_order_by_order_id_service_success(monkeypatch):
# """tests that get_order_by_order_id_service() will successfully get an order given valid order id"""
# # def test_get_order_by_order_id_service_order_not_found(monkeypatch):
# """tests that get_order_by_order_id_service() will generate error if order id not found"""


# # def test_get_orders_by_restaurant_service_success(monkeypatch):
# """tests that get_orders_by_restaurant_service() will successfully get an order given valid restaurant id"""
# # def test_get_orders_by_restaurant_service_not_found(monkeypatch):
# """tests that get_orders_by_restaurant_service() will generate error if restaurant id not found"""
# # def test_get_orders_by_restaurant_service_no_orders(monkeypatch):
# """tests that get_orders_by_restaurant_service() will generate error if no orders match restaurant id"""


# # def test_get_orders_by_userid_service_success(monkeypatch):
# """tests that get_orders_by_userid_service() will successfully get an order given valid user id"""
# # def test_get_orders_by_userid_service_not_found(monkeypatch):
# """tests that get_orders_by_userid_service() will generate error if userid not found"""
# # def test_get_orders_by_restaurant_service_no_orders(monkeypatch):
# """tests that get_orders_by_userid_service() will generate error if no orders match userid"""

# # def test_get_order_status_by_id_service_success(monkeypatch):
# """tests that get_order_status_by_id() will successfully get an order status given a valid order id"""
# # def test_get_order_status_by_id_service_success(monkeypatch):
# """tests that get_order_status_by_id() will generate an error if order not found by order id"""

# # def test_cancel_order_customer_service_success(monkeypatch):
# """tests that cancel_order_customer_service() will successfully cancel an order given valid order id from customer side"""
# # def test_cancel_order_customer_service_order_not_found(monkeypatch):
# """tests that cancel_order_customer_service() will generate an error if order is not found by order id"""
# # def test_cancel_order_customer_service_order_approved(monkeypatch):
# """tests that cancel_order_customer_service() will generate an error if order has already been approved"""


# # def test_cancel_order_restaurant_service_success(monkeypatch):
# """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
# # def test_cancel_order_restaurant_service_order_not_found(monkeypatch):
# """tests that cancel_order_customer_service() will generate an error if order is not found by order id"""
# # def test_cancel_order_restaurant_service_completed(monkeypatch):
# """tests that cancel_order_customer_service() will generate an error if order has already been completed"""


# # def test_accept_order_service_success(monkeypatch):
# """tests that accept_order_service() will successfully accept an order given valid order id from restaurant side"""
# # def test_accept_order_service_order_not_found(monkeypatch):
# """tests that accept_order_service() will generate an error if order is not found by order id"""
# # test_accept_order_service_accepted(monkeypatch):
# """tests that accept_order_service() will generate an error if order has already been accepted"""
