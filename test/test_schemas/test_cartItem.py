from pydantic import ValidationError 
import pytest
from app.schemas.cartItem import CartItemUpdate, CartItemBase, CartItemResponse


def test_CartItemBase_valid(): 
    """Tests valid inputs for CartItemBase"""
    
    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
    }

    result = CartItemBase(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3


def test_CartItemBase_wrong_value(): 
    """Tests invalid inputs for CartItemBase"""

    cartItem_data = { 
        "food_item_id": None,
        "quantity": "3",
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)


def test_CartItemBase_missing_input(): 
    """Tests missing values for CartItemBase"""

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)




def test_CartItemResponse_valid(): 
    """Tests valid inputs for CartItemResponse"""

    cartItem_data = {
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
        "customer_id": "2",
        "address_id": "3",
        "food_item_id": 1.0,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5
    }

    result = CartItemResponse(**cartItem_data)
    assert result.cart_item_id == "0120f079-9e09-4c6f-87fa-e767fa79a62b"
    assert result.cart_id == "e9fffefe-7287-46e4-a433-05f11c73e4a4"
    assert result.food_item_id == 1
    assert result.quantity == 1
    assert result.price_per_item == 15.5
    assert result.address_id == "3"
    assert result.subtotal == 15.5


def test_CartItemResponse_wrong_value(): 
    """Tests invalid values for CartItemResponse"""

    cartItem_data = { 
        "cart_item_id": "200",
        "cart_id": 400,
        "address_id": 33,
        "food_item_id": 1.0,
        "quantity": "3",
        "price_per_item": 2.0,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


def test_CartItemResponse_missing_input(): 
    """Tests missing values for CartItemResponse"""

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)



def test_CartItemUpdate_valid(): 
    """Tests valid inputs for CartItemUpdate"""

    cartItem_data = { 
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "quantity": 1,
        "price_per_item": 15.5,
    }

    result = CartItemUpdate(**cartItem_data)
    assert result.quantity == 1
    assert result.price_per_item == 15.5


def test_CartItemUpdate_zero_value(): 
    """Tests zero value for CartItemUpdate"""

    cartItem_data = { 
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "quantity": 0,
        "price_per_item": 2.0,
    }
    with pytest.raises(ValidationError):
       CartItemUpdate(**cartItem_data)


def test_CartItemUpdate_negative_value(): 
    """Tests negative value for CartItemUpdate"""

    cartItem_data = { 
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "quantity": -1,
        "price_per_item": 2.0,
    }
    with pytest.raises(ValidationError):
       CartItemUpdate(**cartItem_data)


def test_CartItemUpdate_missing_value(): 
    """Tests missing value for CartItemUpdate"""

    cartItem_data = { 
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "quantity": 1,
    }
    with pytest.raises(ValidationError):
       CartItemUpdate(**cartItem_data)