from pydantic import ValidationError
from datetime import datetime
import pytest
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Order import  OrderCreate, OrderBase, OrderResponse
<<<<<<< HEAD
from app.schemas.OrderItem import OrderItemCreate, OrderItemResponse # type: ignore
=======
>>>>>>> main


def test_OrderBase_valid_input():
    """test that OrderBase is created successfully with valid data"""
    input_data = {"restaurant_id" : "1",
                "customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street"}
    result = OrderBase(**input_data)
    assert result.restaurant_id == "1"
    assert result.delivery_address == "268 High Street"
    assert result.customer_id == "44"


def test_OrderBase_invalid_input():
    """test that OrderBase creates an error if it receives in invalid input"""
    input_data = {"restaurant_id" : 45,
                "customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street"}
    with pytest.raises(ValidationError): OrderBase(**input_data)

def test_OrderBase_missing_input():
    """test that OrderBase creates an error if it receives an input with missing field"""
    input_data = {"customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street"}
    with pytest.raises(ValidationError): OrderBase(**input_data)

def test_OrderBase_missing_optional_input():
    """test that OrderBase creates an error if it receives an input with missing optional field"""
    input_data = {"customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street"}
    with pytest.raises(ValidationError): OrderBase(**input_data)
    
def test_OrderCreate_valid_input():
    """test that OrderCreate is created successfully with valid data"""
    input_data = {"restaurant_id" : "1",
                "customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street",
                "cart_id": "999"
                }
    result = OrderCreate(**input_data)
    assert result.restaurant_id == "1"
    assert result.cart_id == "999"
    assert result.delivery_address == "268 High Street"
    assert result.customer_id == "44"

def test_OrderCreate_invalid_input():
    """test that OrderCreate creates an error if it receives in invalid input"""
    input_data = {"restaurant_id" : "1",
                    "customer_id" : 44,
                    "delivery_address_id" : "5",
                    "delivery_address" : "268 High Street",
                    "cart_id": "999",
                    "items": [{
                        "food_item_id": 1,
                        "quantity": 1,
                        "price_per_item": 88.88
                    }]
                    }
    with pytest.raises(ValidationError): OrderCreate(**input_data)

<<<<<<< HEAD
# def test_OrderCreate_no_items():
#     """test that OrderCreate creates an error if it receives an input with no items"""
#     input_data = {"restaurant_id" : 1,
#                     "customer_id" : "44",
#                     "delivery_address_id" : "5",
#                     "delivery_address" : "268 High Street",
#                     "cart_id": "999",
#                     "items": [{
#                 }]
#                 }
#     with pytest.raises(ValidationError): OrderCreate(**input_data)
    
=======
>>>>>>> main
def test_OrderCreate_missing_input():
    """test that OrderCreate creates an error if it receives an input with missing field"""
    input_data = {
                    "customer_id" : "44",
                    "delivery_address_id" : "5",
                    "delivery_address" : "268 High Street",
                    "cart_id": "999"
                    }
    with pytest.raises(ValidationError): OrderCreate(**input_data)
    
def test_OrderResponse_valid_input():
    """test that OrderResponse is created successfully with valid data"""
    input_data = {"restaurant_id" : "45",
                "customer_id" : "44",
                "delivery_address_id" : "5",
                "delivery_address" : "268 High Street",
                "cart_id": "999",
                "items": [{
                    "order_item_id": "1",
                    "order_id": "333",
                    "food_item_id": 1,
                    "quantity": 1,
                    "price_per_item": 88.88
                }],
                "order_id" : "333",
                "created_date" : "2024-02-20T12:34:56",
                "total_amount" : 89.88,
                "delivery_id" : "6",
                "status" : "PENDING"
                }
    result = OrderResponse(**input_data)
    assert result.order_id == "333"
    assert result.created_date == datetime.fromisoformat("2024-02-20T12:34:56")
    assert len(result.items) == 1
    assert result.items[0].food_item_id == 1
    assert result.items[0].order_item_id == "1"    
    assert result.restaurant_id == "45"
    assert result.delivery_address == "268 High Street"
    assert result.customer_id == "44"
    assert result.status == OrderStatus.PENDING

def test_OrderResponse_invalid_input():
    """test that OrderResponse creates an error if it receives in invalid input"""
    input_data = {"restaurant_id" : "45",
                    "customer_id" : "44",
                    "delivery_address_id" : "5",
                    "delivery_address" : "268 High Street",
                    "cart_id": "999",
                    "items": [{
                        "order_item_id": "1",
                        "order_id": "333",
                        "food_item_id": 1,
                        "quantity": 1,
                        "price_per_item": 88.88
                    }],
                    "order_id" : 333,
                    "created_date" : "2024-02-20T12:34:56",
                    "total_amount" : 89.88,
                    "delivery_id" : "6",
                    "status" : "PENDING"
                    }
    with pytest.raises(ValidationError): OrderResponse(**input_data)

def test_OrderResponse_invalid_status():
    """test that OrderResponse creates an error if it receives in invalid status"""
    input_data = {"restaurant_id" : "45",
                    "customer_id" : "44",
                    "delivery_address_id" : "5",
                    "delivery_address" : "268 High Street",
                    "cart_id": "999",
                    "items": [{
                        "order_item_id": "1",
                        "order_id": "333",
                        "food_item_id": 1,
                        "quantity": 1,
                        "price_per_item": 88.88
                    }],
                    "order_id" : "333",
                    "created_date" : "2024-02-20T12:34:56",
                    "total_amount" : 89.88,
                    "delivery_id" : "6",
                    "status" : "Pending"
                    }
    with pytest.raises(ValidationError): OrderResponse(**input_data)

<<<<<<< HEAD
#def test_OrderResponse_missing_input():
"""test that OrderResponse creates an error if it receives an input with missing field"""
=======
>>>>>>> main
def test_OrderResponse_invalid_status():
    """test that OrderResponse creates an error if it receives in invalid status"""
    input_data = {"restaurant_id" : "45",
                    "customer_id" : "44",
                    "delivery_address_id" : "5",
                    "delivery_address" : "268 High Street",
                    "cart_id": "999",
                    "items": [{
                        "order_item_id": "1",
                        "order_id": "333",
                        "food_item_id": 1,
                        "quantity": 1,
                        "price_per_item": 88.88
                    }],
                    "order_id" : "333",
                    "created_date" : "2024-02-20T12:34:56",
                    "delivery_id" : "6",
                    "status" : "PENDING"
                    }
    with pytest.raises(ValidationError): OrderResponse(**input_data)