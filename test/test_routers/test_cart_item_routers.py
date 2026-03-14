from unittest.mock import patch
from app.schemas.cartItem import CartItemAdd
from app.routers.cartItems import add_cart_item_route
import pytest


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

    