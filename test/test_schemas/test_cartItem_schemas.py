from app.schemas.cartItem import CartItemBase, CartItemResponse
from pydantic import ValidationError
import pytest


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

def test_CartItemBase_missing_input(): 

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)





def test_CartItemResponse_valid(): 

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0,
        "cart_item_id": "31",
        "cart_id": "34", 
        "subtotal": 6.0
    }

    result = CartItemResponse(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0
    assert result.cart_item_id == "31"
    assert result.subtotal == 6.0
    assert result.cart_id == "34"


def test_CartItemResponse_missing_input(): 

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


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