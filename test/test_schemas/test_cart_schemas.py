import pytest 
from pydantic import ValidationError
from app.schemas.cart_schema import CartBase, CartResponse, CartCreate, CartUpdate

def test_cart_base_valid(): 
    """Tests adding CartBase with valid data returns what it is supposed to"""
    data = { 
        "customer_id": "string",
        "cart_id": "FJGSJHFGSHJ",
        "cart_items": [], 
        "total": 0.0
    }

    schema = CartBase(**data)

    assert schema.customer_id == "string"
    assert schema.cart_id == "FJGSJHFGSHJ"
    assert schema.cart_items == []
    assert schema.total == 0.0


def test_cart_response_valid(): 
    """Tests adding CartResponse with valid dadta returns what it is supposed to"""
    data = { 
        "customer_id": "string",
        "cart_id": "FJGSJHFGSHJ",
        "cart_items": [], 
        "total": 0.0
    }

    schema = CartResponse(**data)

    assert schema.customer_id == "string"
    assert schema.cart_id == "FJGSJHFGSHJ"
    assert schema.cart_items == []
    assert schema.total == 0.0


def test_cart_create_valid(): 
    """Tests creating a cart with valid data is successful"""
    data = { 
        "food_item_id": 1,
        "quantity": 2
    }

    schema = CartCreate(**data)

    assert schema.food_item_id == 1
    assert schema.quantity == 2

def test_cart_create_zero(): 
    """Tests creating a cart with quantity zero raises an error"""
    with pytest.raises(ValidationError):
        CartCreate(
            food_item_id = 1,
            quantity = 0
        )


def test_cart_create_negative(): 
    """Tests creating a cart with negative value raises an error"""
    with pytest.raises(ValidationError):
        CartCreate(
            food_item_id = 1,
            quantity = -1
        )

def test_cart_create_empty(): 
    """Tests creating a cart with empty value raises an error"""
    with pytest.raises(ValidationError):
        CartCreate(
            food_item_id = None,
            quantity = 1
        )

def test_cart_create_missing(): 
    """Tests creating a cart with missing value raises an error"""
    with pytest.raises(ValidationError):
        CartCreate(
            food_item_id = 1
        )



def test_update_cart_valid(): 
    """Tests updating a cart with valid data is successful"""
    data = { 
        "food_item_id": 1,
        "quantity": 2
    }

    schema = CartUpdate(**data)

    assert schema.food_item_id == 1
    assert schema.quantity == 2

def test_update_cart_zero(): 
    """Tests updating a cart with quantity zero raises an error"""
    with pytest.raises(ValidationError):
        CartUpdate(
            food_item_id = 1,
            quantity = 0
        )


def test_update_cart_negative(): 
    """Tests updating a cart with negative value raises an error"""
    with pytest.raises(ValidationError):
        CartUpdate(
            food_item_id = 1,
            quantity = -1
        )

def test_update_cart_empty(): 
    """Tests updating a cart with empty value raises an error"""
    with pytest.raises(ValidationError):
        CartUpdate(
            food_item_id = None,
            quantity = 1
        )

def test_update_cart_missing(): 
    """Tests updating a cart with missing value raises an error"""
    with pytest.raises(ValidationError):
        CartUpdate(
            food_item_id = 1
        )