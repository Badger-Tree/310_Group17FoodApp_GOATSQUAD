from app.services.cart_service import add_to_cart, create_cart, get_cart_by_customer, calculateSubtotal
from app.schemas.cart_schema import CartCreate, CartResponse
from fastapi import HTTPException
import pytest
from unittest.mock import patch
from app.routers.cart_router import router

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
    
    mock_cart = [{
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }]

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.save_cart", return_value=mock_cart)
    result = create_cart("2")
    assert result["customer_id"] == "2"
    assert result["cart_items"] == []
    assert result["total"] == 0.0
    

def test_create_cart_customer_int(mocker): 
    """Tests that a cart item is added to a cart successfully with customer id as interger."""
    mock_user = MockUser(id="2")
    
    mock_cart = [{
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }]

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.save_cart", return_value=mock_cart)
    result = create_cart(2)
    assert result["customer_id"] == "2"
    assert result["cart_items"] == []
    assert result["total"] == 0.0
 

def test_create_cart_cart_id_valid(mocker): 
    """Tests that the cart_id is generated properly on first create of cart."""
    mock_user = MockUser(id="2")
    
    mock_cart = [{
        "customer_id": "2",
        "cart_id": "AHDJSFHS",
        "cart_items": [],
        "total": 0.0
    }]

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
    first = result.cart_items[0]
    assert first.food_item_id == 2
    assert first.quantity == 3
    assert first.price_per_item == 5.99
    assert first.subtotal == 17.97
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