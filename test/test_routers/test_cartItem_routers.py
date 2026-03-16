from unittest.mock import patch
from fastapi import HTTPException
from app.schemas.cartItem import CartItemAdd
from app.routers.cartItems import get_cart_item_id, update_cart_item
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
        customer_id= "1"
    )

    existing_cart_items_data = [
        {
            "cart_item_id": "92075de6-2b6d-43b8-acef-4b69c3d962f7",
            "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
            "customer_id": "1",
            "food_item_id": 1,
            "quantity": 1,
            "price_per_item": 15.5,
            "address_id": "3", 
            "subtotal": 15.5
        }
    ]

    existing_cart_items = mocker.patch("app.services.cartItems_service.load_all") 
    existing_cart_items.return_value=existing_cart_items_data

    mock_user = mocker.MagicMock()
    mock_user.id = "1"

    mocker.patch(
    "app.services.cartItems_service.get_user_from_session",
    return_value=mock_user
)       
    from app.routers.cartItems import add_cart_item_route
        
    result = add_cart_item_route(cart_item_input)

    assert result.cart_id == "e9fffefe-7287-46e4-a433-05f11c73e4a4"
    assert result.food_item_id == 1
    assert result.quantity == 1
    assert result.price_per_item == 15.5
    assert result.address_id == "1"
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

    mock_user = mocker.MagicMock()
    mock_user.id = "1"

    mocker.patch(
    "app.services.cartItems_service.get_user_from_session",
    return_value=mock_user
) 
    
    from app.routers.cartItems import add_cart_item_route
    result = add_cart_item_route(cart_item_input)

    assert result.food_item_id == 2
    assert result.quantity == 1
    assert result.price_per_item == 5.99
    assert result.address_id == "1"
    assert result.subtotal == 5.99

    assert hasattr(result, "cart_id")  
    assert isinstance(result.cart_id, str)  

    assert hasattr(result, "cart_item_id")
    assert isinstance(result.cart_item_id, str)


def test_update_cart_item_valid(mocker):
    """Tests updating a cart item if the cart already exists"""
    expected_result = { 
        "address": "555",
        "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
        "cart_id": "3",
        "food_item_id": 2,
        "quantity": 5,
        "price_per_item": 3.0,
        "subtotal": 15.0
    }

    mock_router = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_router.return_value = expected_result

    from app.routers.cartItems import update_cart_item
    
    
    result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", 5)

    assert result == expected_result


def test_update_cart_item_id_not_found(mocker):
    """Tests if updating a cart item if the cart does not exist raises an error"""
    cart_item_id = "999"
    responseDetail = f"Cart Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 3.0}
   
    with pytest.raises(HTTPException) as httpExc:
        update_cart_item(cart_item_id, cart_update_data)
   

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


def test_update_cart_item_invalid(mocker):
    """Tests updating a cart item with invalid types still updates the cart"""
    expected_result = [ { 
        "food_item_id": 2,
        "quantity": 5,
        "price_per_item": 3.0,
        "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
        "cart_id": "3",
        "address_id": "3",
        "subtotal": 15.0
    } ]

    mock_router = mocker.patch("app.services.cartItems_service.load_all")
    mock_router.return_value = expected_result

    from app.routers.cartItems import update_cart_item
    
    result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", "5")

    assert result.food_item_id == 2
    assert result.quantity == 5
    assert result.price_per_item == 3.0
    assert result.cart_item_id == "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    assert result.cart_id == "3"
    assert result.address_id == "3"
    assert result.subtotal == 15.0  



def test_update_cart_item_id_zero(mocker):
    
    """Tests updating a cart item with quantity zero raises an error"""
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    quantity = 0
    mock_load = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_load.return_value = [{"cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", "quantity": 0}]
    from app.routers.cartItems import update_cart_item

    update_cart_item(cart_item_id, quantity)


def test_update_cart_item_id_negative(mocker):
    """Tests updating a cart item with a negative raises an error"""
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    quantity = -1

    mocker.patch("app.routers.cartItems.update_cart_item")
   
    with pytest.raises(ValueError) as VE:
        update_cart_item(cart_item_id, quantity)


def test_delete_cart_item(mocker):
    """Tests deleting a cart item deletes the item"""
    expected_result = []
    
    mock_router = mocker.patch("app.routers.cartItems.delete_cart_item")
    mock_router.return_value = expected_result
    from app.routers.cartItems import delete_cart_item
    
    cart_item_id = "7c67321e-3dda-4a69-bde4-baba0b7c7288"
    result = delete_cart_item(cart_item_id)
    assert result == expected_result




    





