from app.services.cart_item_service import add_cart_item
from app.schemas.cart_item_schema import CartItemAdd
from pydantic import ValidationError
import pytest


def test_add_cart_item_valid(): 
    """Tests that adding a cart item with valid data is successful"""
    cart_add = CartItemAdd(
    food_item_id = 1,
    quantity = 1
    )

    price_per_item = 1.0

    result = add_cart_item(cart_add, price_per_item)

    assert result.food_item_id == 1
    assert result.price_per_item == 1.0
    assert result.quantity == 1
    assert result.subtotal == 1.0

def test_add_cart_item_empty():
    """Tests that adding a cart item with empty data raises and error"""
    with pytest.raises(ValidationError):
        CartItemAdd(food_item_id=None, quantity=None)
   

def test_add_cart_item_zero():
    """Tests that adding a cart item with zero quantity raises an error"""
    with pytest.raises(ValidationError):
        CartItemAdd(food_item_id=1, quantity=0)

