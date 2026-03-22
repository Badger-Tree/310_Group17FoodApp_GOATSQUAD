import pytest 
from pydantic import ValidationError
from app.schemas.cart_item_schema import CartItemBase, CartItemResponse, CartItemAdd

def test_cart_item_base_valid(): 
    """Tests adding a CartItemBase with valid data returns what its supposed to"""
    data = { 
        "cart_item_id": "FGHSFGHSFSH",
        "food_item_id": 1,
        "quantity": 1, 
        "price_per_item": 5.99,
        "subtotal": 5.99
    }

    schema = CartItemBase(**data)

    assert schema.cart_item_id == "FGHSFGHSFSH"
    assert schema.food_item_id == 1
    assert schema.quantity == 1
    assert schema.price_per_item == 5.99
    assert schema.subtotal == 5.99


def test_cart_item_response_valid(): 
    """Tests adding a CartItemResponse with valid data returns what its supposed to"""
    data = { 
        "cart_item_id": "FGHSFGHSFSH",
        "food_item_id": 1,
        "quantity": 1, 
        "price_per_item": 5.99,
        "subtotal": 5.99
    }

    schema = CartItemResponse(**data)

    assert schema.cart_item_id == "FGHSFGHSFSH"
    assert schema.food_item_id == 1
    assert schema.quantity == 1
    assert schema.price_per_item == 5.99
    assert schema.subtotal == 5.99


def test_cart_item_add_valid(): 
    """Tests adding a cart item adds the item successfully"""
    data = { 
        "food_item_id": 1,
        "quantity": 2
    }

    schema = CartItemAdd(**data)

    assert schema.food_item_id == 1
    assert schema.quantity == 2

def test_cart_item_add_zero(): 
    """Tests adding a cart item with zero quantity raises an error"""
    with pytest.raises(ValidationError):
        CartItemAdd(
            food_item_id = 1,
            quantity = 0
        )


def test_cart_item_add_negative(): 
    """Tests adding a cart item with negative quantity raises an error"""
    with pytest.raises(ValidationError):
        CartItemAdd(
            food_item_id = 1,
            quantity = -1
        )

def test_cart_item_add_empty(): 
    """Tests adding an empty value for food_item_id raises an error"""
    with pytest.raises(ValidationError):
        CartItemAdd(
            food_item_id = None,
            quantity = 1
        )

def test_cart_create_missing(): 
    """Tests adding a cart item with missing value raises an error"""
    with pytest.raises(ValidationError):
        CartItemAdd(
            food_item_id = 1
        )