from app.services.cart_item_service import add_cart_item, delete_cart_item, update_cart_item
from app.schemas.cart_item_schema import CartItemAdd
from app.schemas.cart_schema import CartResponse, CartUpdate
from pydantic import ValidationError
import pytest
from fastapi import HTTPException


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


def test_delete_cart_item_valid(): 
    """Tests that deleting a cart item with valid data is successful"""

    cart_delete = CartResponse(
        customer_id = "DHJKHDKJSHDJ",
        cart_id = "SJKHFJKHSFK",
        
        cart_items = [
        {
        "cart_item_id": "CARTITEMDELETE",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

        {
        "cart_item_id": "CARTITEMKEEP",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

    ],
        total = 0.0
    )

    cart_item_id = "CARTITEMDELETE"

    result = delete_cart_item(cart_delete, cart_item_id)

    assert result.customer_id == "DHJKHDKJSHDJ"
    assert result.cart_id == "SJKHFJKHSFK"
    first = result.cart_items[0]
    assert first.cart_item_id == "CARTITEMKEEP"
    assert first.food_item_id == 1
    assert first.price_per_item == 2.0
    assert first.quantity == 1
    assert first.subtotal == 2.0

def test_delete_cart_item_does_not_exist():
    """Tests that deleting a cart item with a cart item id that does not exists raises an error"""
    cart_delete = CartResponse(
        customer_id = "DHJKHDKJSHDJ",
        cart_id = "SJKHFJKHSFK",
        
        cart_items = [
        {
        "cart_item_id": "CARTITEMDELETE",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

        {
        "cart_item_id": "CARTITEMKEEP",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

    ],
        total = 0.0
    )
    
    cart_item_id = "CARTITEMDOESNOTEXIST"
    
    with pytest.raises(HTTPException):
        delete_cart_item(cart_delete, cart_item_id)
   

def test_delete_cart_item_empty():
    """Tests that deleting a cart item with a cart item id that is empty raises an error"""
    cart_delete = CartResponse(
        customer_id = "DHJKHDKJSHDJ",
        cart_id = "SJKHFJKHSFK",
        
        cart_items = [
        {
        "cart_item_id": "CARTITEMDELETE",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

        {
        "cart_item_id": "CARTITEMKEEP",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

    ],
        total = 0.0
    )
    
    cart_item_id = ""
    
    with pytest.raises(HTTPException):
        delete_cart_item(cart_delete, cart_item_id)


def test_update_cart_item_valid(): 
    """Tests that updating a cart item with valid data is successful"""

    cart_current = CartResponse(
        customer_id = "DHJKHDKJSHDJ",
        cart_id = "SJKHFJKHSFK",
        
        cart_items = [
        {
        "cart_item_id": "CARTITEMUPDATE",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

        {
        "cart_item_id": "CARTITEM",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

    ],
        total = 4.0
    )

    item_update = CartUpdate(
        food_item_id = 1,
        quantity = 3
    )

    cart_item_id = "CARTITEMUPDATE"
    price_per_item = 2.0

    result = update_cart_item(cart_current, cart_item_id, price_per_item, item_update)

    assert result.customer_id == "DHJKHDKJSHDJ"
    assert result.cart_id == "SJKHFJKHSFK"
    first = result.cart_items[0]
    assert first.cart_item_id == "CARTITEMUPDATE"
    assert first.food_item_id == 1
    assert first.price_per_item == 2.0
    assert first.quantity == 3
    assert first.subtotal == 6.0

def test_update_cart_item_id_invalid(): 
    """Tests that updating a cart item with invalid cart_item_id raises error"""

    cart_current = CartResponse(
        customer_id = "DHJKHDKJSHDJ",
        cart_id = "SJKHFJKHSFK",
        
        cart_items = [
        {
        "cart_item_id": "CARTITEMINVALID",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

        {
        "cart_item_id": "CARTITEM",
        "food_item_id": 1,
        "price_per_item": 2.0,
        "quantity": 1,
        "subtotal": 2.0
        },

    ],
        total = 4.0
    )

    item_update = CartUpdate(
        food_item_id = 100,
        quantity = 3
    )

    cart_item_id = "CARTITEMUPDATE"
    price_per_item = 2.0

    with pytest.raises(HTTPException):
        update_cart_item(cart_current, cart_item_id, price_per_item, item_update)

