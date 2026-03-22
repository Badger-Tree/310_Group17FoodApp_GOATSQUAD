from app.services.cart_service import add_to_cart, create_cart, get_cart_by_customer, cart_append, calculateSubtotal
from app.schemas.cart_schema import CartCreate, CartResponse
from app.schemas.User import UserResponse
from fastapi import HTTPException
import pytest
from fastapi import FastAPI
from unittest.mock import patch
from app.routers.cart_router import router
from fastapi.testclient import TestClient

mock_data = [{ 
    "customer_id": "2", 
    "cart_id": "GHDJDKSLAJ",
    "cart_items": [],
    "total": 0
}]


def test_get_cart_by_customer_valid(mocker): 
    """Tests getting a cart with a customer id that exists returns the cart successfully"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    result = get_cart_by_customer("2")

    assert result.customer_id == "2"
    assert result.cart_id == "GHDJDKSLAJ"
    assert result.cart_items == []
    assert result.total == 0


def test_get_cart_by_customer_does_not_exist(mocker): 
    """Tests getting a cart by a customer that does not exist raises an error"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    with pytest.raises(HTTPException) as testException: 
        get_cart_by_customer("200")

    assert testException.value.status_code ==404


def test_get_cart_by_customer_int(mocker): 
    """Tests getting a cart with a customer id as an interger returns the cart successfully"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    result = get_cart_by_customer(2)

    assert result.customer_id == "2"
    assert result.cart_id == "GHDJDKSLAJ"
    assert result.cart_items == []
    assert result.total == 0


class MockUser:
    def __init__(self, id):
        self.id = id

def test_create_cart_valid(mocker): 
    """Tests that a cart item is added to a cart successfully with a valid customer id."""
    mock_user = MockUser(id="2")
    
    mock_cart = {
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.save_cart", return_value=mock_cart)
    result = create_cart("2")
    assert result["customer_id"] == "2"
    assert result["cart_items"] == []
    assert result["total"] == 0.0
    

def test_create_cart_customer_int(mocker): 
    """Tests that a cart item is added to a cart successfully with customer id as interger."""
    mock_user = MockUser(id="2")
    
    mock_cart = {
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.save_cart", return_value=mock_cart)
    result = create_cart(2)
    assert result["customer_id"] == "2"
    assert result["cart_items"] == []
    assert result["total"] == 0.0
 

def test_create_cart_cart_id_valid(mocker): 
    """Tests that the cart_id is generated properly on first create of cart."""
    mock_user = MockUser(id="2")
    
    mock_cart = {
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.save_cart", return_value=mock_cart)
    result = create_cart(2)
    assert isinstance(result["cart_id"], str)
    assert len(result["cart_id"]) > 0 








mock_data = [
        {
            "customer_id": "2",
            "cart_id": "GHDJDKSLAJ", 
            "cart_items": [],
            "total": 0.0
        }
    ]
    
cart_data = CartCreate(food_item_id = 2, quantity = 3) 

customer_id = "2"

def test_add_to_cart_valid(mocker): 
    """Tests that a cart item is added to a cart successfully."""

    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    result = add_to_cart(customer_id, cart_data)

    assert result.customer_id == "2"
    assert result.cart_id == "GHDJDKSLAJ" 
    assert result.cart_items[0].food_item_id == 2
    assert result.cart_items[0].quantity == 3
    assert result.cart_items[0].price_per_item == 5.99
    assert result.cart_items[0].subtotal == 17.97
    assert result.total == 17.97


def test_add_to_cart_no_food_item(mocker): 
    """Tests that an exception is raised when the food_item_id does not exist"""
    cart_data = CartCreate(food_item_id = 100, quantity = 3) 
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    with pytest.raises(HTTPException) as testException: 
        add_to_cart(customer_id, cart_data)

    assert testException.value.status_code ==404


def test_add_to_cart_no_customer_id(mocker): 
    """Tests that an exception is raised when the customer_id does not exist"""

    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    with pytest.raises(HTTPException) as testException: 
        add_to_cart("100", cart_data)

    assert testException.value.status_code ==404


def test_add_to_cart_invalid(mocker): 
    """Tests that an exception is raised when inavlid data is added to the cart"""

    cart_data = CartCreate(food_item_id = "100", quantity = "3")
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data)
    with pytest.raises(HTTPException) as testException: 
        add_to_cart("100", cart_data)

    assert testException.value.status_code ==404





mocker_data = [
    {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [
            {
                "cart_item_id": "01KM8SQ4JB61NVWKSM2AVSFN3C",
                "food_item_id": 2,
                "quantity": 3,
                "price_per_item": 5.99,
                "subtotal": 17.97
            }
        ],
        "total": 17.97
    }
]

cart_response = CartResponse(
        customer_id= "2",
        cart_id= "GHDJDKSLAJ",
        cart_items= [
            {
                "cart_item_id": "61NVWKSM2AVSFDFKSLAJA",
                "food_item_id": 1,
                "quantity": 1,
                "price_per_item": 15.5,
                "subtotal": 15.5
            }
        ], 
        total = 15.5
    ) 


def test_cart_append_valid(mocker): 
    """Tests that appending to a cart returns the old items as well as the newly added item"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mocker_data)
    result = cart_append(mocker_data, cart_response)
    
    cart = result[0]
    assert cart["customer_id"] == "2"
    assert cart["cart_id"]== "GHDJDKSLAJ"
    first = cart["cart_items"][0]
    assert first["food_item_id"] == 2
    assert first["quantity"] == 3
    assert first["price_per_item"] == 5.99
    assert first["subtotal"] == 17.97

    second = cart["cart_items"][1]
    assert second.food_item_id == 1
    assert second.quantity == 1
    assert second.price_per_item == 15.5
    assert second.subtotal == 15.5
    assert cart["total"] == 33.47




mocker_data_empty = [
    {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [
            {
                "cart_item_id": "01KM8SQ4JB61NVWKSM2AVSFN3C",
                "food_item_id": 2,
                "quantity": 3,
                "price_per_item": 5.99,
                "subtotal": 17.97
            }
        ],
        "total": 17.97
    }
]

cart_response_empty = CartResponse(
        customer_id= "2",
        cart_id= "GHDJDKSLAJ",
        cart_items= [],
        total = 0.0
    ) 

def test_cart_append_empty(mocker): 
    """Tests that appending to cart with empty cart_items does not change the cart content"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mocker_data_empty)

    result = cart_append(mocker_data_empty, cart_response_empty)
    cart = result[0]
    assert cart["customer_id"] == "2"
    assert cart["cart_id"]== "GHDJDKSLAJ" 
    first = cart["cart_items"][0]
    assert first["food_item_id"] == 2
    assert first["quantity"] == 3
    assert first["price_per_item"] == 5.99
    assert first["subtotal"] == 17.97
    assert cart["total"] == 17.97


def test_cart_append_duplicate_items(mocker):
    """Checks if appending duplicate items adds the total correctly"""
    existing_cart = [
        {
        "customer_id": "2",
        "cart_id": "FHJSHFKJSHF",
        "cart_items": [{
            "cart_item_id": "DHJKSHDJSH",
            "food_item_id": 1, 
            "quantity": 2, 
            "price_per_item": 5.0, 
            "subtotal": 10.0
            }],
        "total": 10.0
        }
    ]
    new_cart = CartResponse(
        customer_id="2",
        cart_id="FHJSHFKJSHF",
        cart_items=[{"cart_item_id": "DHJKSHDJSH","food_item_id": 1, "quantity": 3, "price_per_item": 5.0, "subtotal": 15.0}],
        total=15.0
    )

    result = cart_append(existing_cart, new_cart)
    cart = result[0]
    assert len(cart["cart_items"]) == 2  
    assert cart["total"] == 25.0 






mock_current_cart = [
    {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [
            {
                "cart_item_id": "01KM8SQ4JB61NVWKSM2AVSFN3C",
                "food_item_id": 2,
                "quantity": 3,
                "price_per_item": 5.99,
                "subtotal": 17.97
            },

             {
                "cart_item_id": "61NVWKSM2AVSFDFKSLAJA",
                "food_item_id": 1,
                "quantity": 1,
                "price_per_item": 15.5,
                "subtotal": 15.5
            }
        ],
        "total": 33.47
    }
]

def test_CalculateSubtotal_valid(mocker): 
    """Tests that calculatesubtotal calculates what its supposed to with valid data"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_current_cart)

    result = calculateSubtotal(mock_current_cart[0])
    assert result == 33.47

def test_CalculateSubtotal_zero(mocker): 
    """Tests that calculatesubtotal returns 0 if cart_items are empty"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = [])

    result = calculateSubtotal({"cart_items": []})
    assert result == 0.0

def test_CalculateSubtotal_empty(mocker): 
    """Tests that calculatesubtotal returns 0 when the cart is empty"""
    mocker.patch("app.services.cart_service.load_all_carts", return_value = [])

    cart = {}
    result = calculateSubtotal(cart)
    assert result == 0.0