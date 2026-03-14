from unittest.mock import patch
from fastapi import HTTPException
from app.schemas.cartItem import CartItemAdd
from app.routers.cartItems import get_cart_item_id, add_cart_item_route
import pytest


def test_get_cart_item_id_valid(mocker):
    """Tests successful path where cart_item_id is found"""
    mock_router = mocker.patch("app.routers.cartItems.get_cartItem_by_id")
    mock_router.return_value = {"cart_item_id": "300"}
    result = get_cart_item_id("300")

    assert result["cart_item_id"] == "300"


def test_get_cart_item_id_not_found(mocker):
    """Tests unsuccessful path where cart_item_id is not found"""
    cart_item_id = "999"
    mock_router = mocker.patch("app.routers.cartItems.get_cartItem_by_id")
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        get_cart_item_id("999")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


def test_add_cart_item_route_exists(mocker):
    """Tests adding a cart item for a customer if the cart already exists"""
    
    cart_item_input = CartItemAdd(
        food_item_id= 1,
        quantity= 1,
        customer_id= "2"
    )

    existing_cart_items_data = [
        {
            "cart_item_id": "92075de6-2b6d-43b8-acef-4b69c3d962f7",
            "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
            "customer_id": "2",
            "food_item_id": 1,
            "quantity": 1,
            "price_per_item": 15.5,
            "address_id": "3", 
            "subtotal": 15.5
        }
    ]

    existing_cart_items = mocker.patch("app.services.cartItems_service.load_all") 
    existing_cart_items.return_value=existing_cart_items_data
        
    result = add_cart_item_route(cart_item_input)

    assert result.cart_id == "e9fffefe-7287-46e4-a433-05f11c73e4a4"
    assert result.food_item_id == 1
    assert result.quantity == 1
    assert result.price_per_item == 15.5
    assert result.address_id == "3"
    assert result.subtotal == 15.5

    assert hasattr(result, "cart_item_id")
    assert isinstance(result.cart_item_id, str)



def test_add_cart_item_route_does_not_exist(mocker):
    """Tests adding a cart item for a customer if the cart does not exist"""
    
    cart_item_input = CartItemAdd(
        food_item_id= 2,
        quantity= 1,
        customer_id= "3"
    )


    existing_cart_items_data = [
        {
            "cart_item_id": "92075de6-2b6d-43b8-acef-4b69c3d962f7",
            "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
            "customer_id": "3",
            "food_item_id": 2,
            "quantity": 1,
            "price_per_item": 5.99,
            "address_id": "4", 
            "subtotal": 5.99
        }
    ]

    not_existing_cart_items = mocker.patch("app.services.cartItems_service.load_all") 
    not_existing_cart_items.return_value=existing_cart_items_data
    result = add_cart_item_route(cart_item_input)

    assert result.food_item_id == 2
    assert result.quantity == 1
    assert result.price_per_item == 5.99
    assert result.address_id == "4"
    assert result.subtotal == 5.99

    assert hasattr(result, "cart_id")  
    assert isinstance(result.cart_id, str)  

    assert hasattr(result, "cart_item_id")
    assert isinstance(result.cart_item_id, str)

    





