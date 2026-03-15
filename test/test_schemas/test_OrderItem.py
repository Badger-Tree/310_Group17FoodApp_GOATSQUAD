from datetime import datetime
from pydantic import ValidationError
import pytest
from app.schemas.Order import  OrderCreate, OrderBase, OrderResponse
from app.schemas.OrderItem import OrderItemBase, OrderItemCreate, OrderItemResponse # type: ignore


def test_OrderItemBase_valid():
    """test that OrderItemBase is created successfully with valid data"""
    input_data = {"food_item_id": 123,
                "quantity" : 1,
                  "price_per_item" : 5.99}
    result = OrderItemBase(**input_data)
    assert result.food_item_id == 123
    assert result.quantity == 1
    assert result.price_per_item == 5.99

def test_OrderItemBase_invalid_data():
    """test that OrderItemBase creates an error if it receives in invalid input"""
    input_data = {"food_item_id": 123,
                  "quantity" : "one",
                  "price_per_item" : 5.99}
    with pytest.raises(ValidationError): OrderItemBase(**input_data)


def test_OrderItemBase_missing_data():
    """test that OrderItemBase creates an error if it receives an input with missing field"""
    input_data = {"food_item_id": 123,
                "price_per_item" : 5.99}
    with pytest.raises(ValidationError): OrderItemBase(**input_data)
    
    
# def test_OrderItemCreate_valid():
    """test that OrderItemCreate is created successfully with valid data"""
    input_data = {"food_item_id": 123,
                "quantity" : 5,
                "price_per_item" : 0.5}
    result = OrderItemCreate(**input_data)
    assert result.food_item_id == 123
    assert result.quantity == 5
    assert result.price_per_item == 0.5
    
def test_OrderItemCreate_invalid_data():
    """test that OrderItemCreate creates an error if it receives in invalid input"""
    input_data = {"food_item_id": 123,
                  "quantity" : 5.6,
                  "price_per_item" : 5.99}
    with pytest.raises(ValidationError): OrderItemCreate(**input_data)

def test_OrderItemCreate_missing_data():
    """test that OrderItemCreate creates an error if it receives an input with missing field"""
    input_data = {"food_item_id": 123,
                  "quantity" : 5.6,}
    with pytest.raises(ValidationError): OrderItemCreate(**input_data)

def test_OrderItemResponse_valid():
    """test that OrderItemResponse is created successfully with valid data"""
    input_data = {"food_item_id": 123,
                "quantity" : 1,
                "price_per_item" : 5.99,
                "order_item_id" : "55",
                "order_id" : "987"}
    result = OrderItemResponse(**input_data)
    assert result.food_item_id == 123
    assert result.quantity == 1
    assert result.price_per_item == 5.99
    assert result.order_item_id == "55"
    assert result.order_id == "987"
        
def test_OrderItemResponse_invalid_data():
    """test that OrderItemResponse creates an error if it receives in invalid input"""
    input_data = {"food_item_id": 123.6,
                "quantity" : 1,
                "price_per_item" : 5.99,
                "order_item_id" : "55",
                "order_id" : "987"}
    with pytest.raises(ValidationError): OrderItemResponse(**input_data)

def test_OrderItemResponse_missing_data():
    """test that OrderItemResponse creates an error if it receives an input with missing field"""
    input_data = {"food_item_id": 123,
                "quantity" : 1,
                "price_per_item" : 5.99,
                "order_id" : "987"}
    with pytest.raises(ValidationError): OrderItemResponse(**input_data)