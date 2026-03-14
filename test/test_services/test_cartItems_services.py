import pytest
from fastapi import HTTPException
from app.routers.cartItems import update_cart_item, delete_cart_item
from unittest.mock import patch


def test_update_cart_item_valid():
    """Tests that the function returns proper data with valid input"""
    
    payload = {
        "quantity": 1, 
        "price_per_item": 2.0
        }

    mock_data = [
        {
            "address_id": "5",
            "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
            "cart_id": "3",
            "food_item_id": 2,
            "quantity": 1,
            "price_per_item": 2.0,
            "subtotal": 2.0
        }
    ]

    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", payload)

    assert result.address_id == "5"
    assert result.cart_item_id == "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    assert result.cart_id == "3"
    assert result.food_item_id == 2
    assert result.quantity == 1
    assert result.price_per_item == 2.0
    assert result.subtotal == 2.0


def test_update_cart_item_id_not_found(mocker):
    """Tests function raises an error when the cart to update is not found"""
    cart_item_id = "999"
    responseDetail = f"Cart Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.services.cartItems_service.update_cartItem")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 3}
   
    with pytest.raises(HTTPException) as httpExc:
        update_cart_item(cart_item_id, cart_update_data)
   
    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


def test_update_cart_item_invalid():
    """Tests cart is properly updated even with inproper input i.e string instead of int"""
    payload = {
        "quantity": "5", 
        "price_per_item": "3.0"
        }

    mock_data = [
        {
        "address_id": "5",
        "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
        "cart_id": "3",
        "food_item_id": 2,
        "quantity": 5,
        "price_per_item": 3.0,
        "subtotal": 15.0
        }
    ]

    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", payload)

    assert result.address_id == "5"
    assert result.cart_item_id == "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    assert result.cart_id == "3"
    assert result.food_item_id == 2
    assert result.quantity == 5
    assert result.price_per_item == 3.0
    assert result.subtotal == 15.0


def test_update_cart_item_id_zero():
    """Tests that if the quantity is zero it raises an error"""
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    
    cart_update_data = { 
        "quantity": 0,
        "price_per_item": 2.0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data)


def test_update_cart_item_id_zeros():
    """Tests that if the quantity is less than zero it raises an error """
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    
    cart_update_data = { 
        "quantity": -1,
        "price_per_item": 0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data)



def test_remove_cartItem_valid(): 
    """Tests that the cart_item_id in question is removed"""
    cart_item_id = "7c67321e-3dda-4a69-bde4-baba0b7c7288"

    mock_data = [{
        "cart_item_id": cart_item_id,
        "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
        "customer_id": "2",
        "address_id": "3",
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5
  }]
    
    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = delete_cart_item(cart_item_id)

    assert result == None


def test_remove_cartItem_invalid(mocker): 
    """Tests that if the cart does not exist it raises an exception"""

    cart_item_id = "7c67321e-3dda-4a69-bde4-baba0b7c7288"
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.services.cartItems_service.update_cartItem")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
    
    with pytest.raises(HTTPException) as httpExc:
        delete_cart_item(cart_item_id)
   

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail
    
