from unittest.mock import patch
from fastapi import HTTPException
from app.routers.carts import get_cart_by_id_service, get_items_by_carts, add_cart
from app.schemas.cart import CartBase
import pytest


mock_cart_data = {
  "cart_id": "3fd5aa2e-d908-3fe2-b2ce-d67abf97e862",
  "customer_id": "2"
}

def test_get_cart_by_id_valid(mocker):
    """Tests successful path where cart_id is found"""
    cart_id = "3fd5aa2e-d908-3fe2-b2ce-d67abf97e862"
    customer_id = "2"
    mocker.patch(
        "app.services.cart_services.load_all",
        return_value=[{"cart_id": cart_id, "customer_id": customer_id}]
    )
    result = get_cart_by_id_service(cart_id)

    assert result.cart_id == cart_id
    assert result.customer_id == customer_id

def test_get_cart_id_not_found(mocker):
    """Tests unsuccessful path where cart_id is not found"""
    cart_id = "999"
    mock_router = mocker.patch("app.services.cart_services.load_all")
    responseDetail = f"Cart '{cart_id}' not found"
    statusCode = 404
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        get_cart_by_id_service("999")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail

mock_cart_data = {
  "cartList": [
      {
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 5.99,
        "address_id": "3",
        "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
        "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
        "subtotal": 5.99
      },
      {
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "address_id": "3",
        "cart_item_id": "1120f079-9e09-4c6f-87fa79a62b",
        "cart_id": "f9fffefe-7287-46e4-a433-05f11c73e4a4",
        "subtotal": 15.5
      }
    ],
  "total": 21.49
}


expected_cart_items = {
    "cartList": [mock_cart_data["cartList"][0]],
    "total": 5.99
}


def test_get_items_by_carts_valid(mocker):
    """Tests successful path where cart_id items are found"""
    mock_router = mocker.patch("app.services.cart_services.load_all_cart_items") 
    mock_router.return_value = mock_cart_data["cartList"]
    result = get_items_by_carts("e9fffefe-7287-46e4-a433-05f11c73e4a4")
    assert result == expected_cart_items


def test_get_items_by_carts_not_found(mocker):
    """Tests unsuccessful path where cart_id items are not found"""
    cart_id = "999"
    mock_router = mocker.patch("app.services.cartItems_service.load_all")
    responseDetail = f"Cart '{cart_id}' not found"
    statusCode = 404
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_carts("999")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


mocker_data = { 
    "cart_id": "333", 
    "customer_id": "99" 
    }
expected_data = { 
    "cart_id": "333",
    "customer_id": "99"
}

def test_add_cart(mocker): 
    """Tests adding a cart creates a new cart with cart_id and customer_id"""
    cart = CartBase(cart_id='333', customer_id='99')
    mock_router = mocker.patch("app.services.cart_services.load_all_cart_items")
    mock_router.return_value = mocker_data
    result = add_cart(cart)
    assert result == expected_data


def test_add_cart_empty(mocker):
    """Tests trying to add empty values results in an exception"""
    cart = CartBase(cart_id='', customer_id='')
    mock_router = mocker.patch("app.services.cart_services.load_all_cart_items")
    responseDetail = "customer_id cannot be empty"
    statusCode = 400
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        add_cart(cart)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail




