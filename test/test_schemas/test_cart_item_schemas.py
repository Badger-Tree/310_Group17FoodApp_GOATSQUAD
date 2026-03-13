from pydantic import ValidationError 
import pytest
from app.schemas.cartItem import CartItemAdd


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

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "customer_id": 500
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)


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

    cartItem_data = { 
        "food_item_id": 1,
        "quantity": 0,
        "customer_id": 500
    }
    with pytest.raises(ValidationError):CartItemAdd(**cartItem_data)