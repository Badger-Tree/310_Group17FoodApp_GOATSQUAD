from pydantic import ValidationError 
import pytest
from app.schemas.cartItem import CartItemBase, CartItemResponse


"""Confirms the model stored each field with valid data"""

def test_CartItemBase_valid(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0
    }

    result = CartItemBase(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0


"""Confirms the model raises exception with invalid data"""

def test_CartItemBase_wrong_value(): 

    cartItem_data = { 
        "food_item_id": None,
        "quantity": "3",
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)


"""Confirms the model raises exception with missing data"""

def test_CartItemBase_missing_input(): 

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)


"""Ensures response contains required fields with valid data"""


def test_CartItemResponse_valid(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0,
        "cart_item_id": "31",
        "cart_id": "22",
        "subtotal": 6.0
    }

    result = CartItemResponse(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0
    assert result.cart_item_id == "31"
    assert result.cart_id == "22"
    assert result.subtotal == 6.0


"""Ensures response raises error with invalid data"""

def test_CartItemResponse_wrong_value(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": "3",
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


"""Ensures response raises error with missing data"""

def test_CartItemResponse_missing_input(): 

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)

"""Ensures response raises error with zero data"""

def test_CartItemResponse_zero_value(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 0,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


"""Ensures response raises error with negative data"""

def test_CartItemResponse_negative_value(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": -1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)
