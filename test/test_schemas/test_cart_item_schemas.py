from pydantic import ValidationError 
import pytest
from app.schemas.cartItem import CartItemAdd


def test_CartItemBase_valid(): 
    """Confirms the model stored each field with valid data"""
    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0
    }

    result = CartItemBase(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0


def test_CartItemBase_wrong_value(): 
    """Confirms the model raises exception with invalid data"""

    cartItem_data = { 
        "food_item_id": None,
        "quantity": "3",
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)


def test_CartItemBase_missing_input(): 
    """Confirms the model raises exception with missing data"""

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemBase(**cartItem_data)






def test_CartItemResponse_valid(): 
    """Ensures response contains required fields with valid data"""

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,

        "customer_id": 500
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)



def test_CartItemResponse_wrong_value(): 
    """Ensures response raises error with invalid data"""

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



def test_CartItemResponse_missing_input(): 
    """Ensures response raises error with missing data"""

    cartItem_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


def test_CartItemResponse_zero_value(): 
    """Ensures response raises error with zero data"""

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 0,
        "customer_id": 500
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)

    cartItem_data = {
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartItemResponse(**cartItem_data)


def test_CartItemResponse_negative_value(): 
    """Ensures response raises error with negative data"""

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





def test_CartItemAdd_valid(): 
    """Tests valid inputs for CartItemAdd"""

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "customer_id": "c1"
    }

    result = CartItemAdd(**cartItem_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.customer_id == "c1"


def test_CartItemAdd_wrong_value(): 
    """Tests invalid inputs for CartItemAdd"""
    
from app.schemas.cartItem import CartItemBase, CartItemResponse


def test_CartItemAdd_missing_input(): 
    """Tests missing input for CartItemAdd"""

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)


def test_CartItemAdd_negative_value(): 
    """Tests negative values for CartItemAdd"""

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": -1,
        "customer_id": 500
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)


def test_CartItemAdd_zero_value(): 
    """Tests zero values for CartItemAdd"""

    cartItem_data = {"price_per_item": 2.0,
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



