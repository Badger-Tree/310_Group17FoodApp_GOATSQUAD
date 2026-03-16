from pydantic import ValidationError 
import pytest
from app.schemas.cart import CartBase, CartResponse, ListCartResponse


def test_CartBase_valid(): 
    """Tests valid inputs for CartBase"""
    
    cart_data = { 
        "cart_id": "1",
        "customer_id": "3",
    }

    result = CartBase(**cart_data)
    assert result.cart_id == "1"
    assert result.customer_id == "3"


def test_CartBase_wrong_value(): 
    """Tests invalid inputs for CartBase"""

    cart_data = { 
        "cart_id": None,
        "customer_id": 3,
    }
    with pytest.raises(ValidationError):
       CartBase(**cart_data)


def test_CartBase_missing_input(): 
    """Tests missing values for CartBase"""

    cart_data = { 
        "cart_id": 1,
    }
    with pytest.raises(ValidationError):
       CartBase(**cart_data)





def test_CartResponse_valid(): 
    """Tests valid inputs for CartResponse"""

    cart_data = {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5
    }

    result = CartResponse(**cart_data)
    assert result.cart_id == "2"
    assert result.customer_id == "2"
    assert result.cart_item_id == "3"
    assert result.food_item_id == 1
    assert result.quantity == 1
    assert result.price_per_item == 15.5
    assert result.subtotal == 15.5


def test_CartResponse_wrong_value(): 
    """Tests invalid values for CartResponse"""

    cart_data = { 
        "cart_item_id": "200",
        "cart_id": 400,
        "customer_id": 33,
        "food_item_id": 1.0,
        "quantity": "3",
        "price_per_item": 2.0,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)


def test_CartResponse_missing_input(): 
    """Tests missing values for CartResponse"""

    cart_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)


def test_CartResponse_zero_value(): 
    """Ensures response raises error with zero data"""

    cart_data = {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": 0,
        "price_per_item": 15.5,
        "subtotal": 0
    }
    with pytest.raises(ValidationError):
        CartResponse(**cart_data)

    cart_data = {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 0,
        "subtotal": 0
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)


def test_CartResponse_negative_value(): 
    """Ensures response raises error with negative data"""

    cart_data = {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": -1,
        "price_per_item": 15.5,
        "subtotal": 15.5
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)


def test_ListCartResponse_valid(): 
    """Tests valid inputs for ListCartResponse"""

    cart_data = {
    "cartList": [
    {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5,
    }
    ], 
        "total": 15.5
    }

    result = ListCartResponse(**cart_data)
    assert result.total == 15.5

def test_ListCartResponse_wrong_values(): 
    """Tests invalid inputs for ListCartResponse raises an error"""

    cart_data = {
    "cartList": [
    {
        "cart_id": "2",
        "customer_id": 2,
        "cart_item_id": 3,
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5,
    }
    ], 
        "total": 15.5
    }

    with pytest.raises(ValidationError):
       ListCartResponse(**cart_data)


def test_zero_values(): 
    """Ensures zero value raises an error"""

    cart_data = {
    "cartList": [
    {
        "cart_id": "2",
        "customer_id": "2",
        "cart_item_id": "3",
        "food_item_id": 1,
        "quantity": 0,
        "price_per_item": 15.5,
        "subtotal": 0,
    }
    ], 
        "total": 0.0
    }

    with pytest.raises(ValidationError):
       ListCartResponse(**cart_data)