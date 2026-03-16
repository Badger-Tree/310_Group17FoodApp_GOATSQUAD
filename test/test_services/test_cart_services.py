import pytest
from fastapi import HTTPException
from app.services.cart_services import get_items_by_cart, create_cart
from unittest.mock import patch
 

mocker_cart_data = [ { 
    "cart_id": "6",
    "customer_id": "1"
}]


from app.services.cart_services import get_cart_by_id_service

def test_get_cart_by_id_service_valid(mocker):
    """Checks that the function returns the correct dictionary with valid data on request of the cart id"""

    mocker.patch("app.services.cart_services.load_all", return_value=mocker_cart_data)
    result = get_cart_by_id_service("6")

    assert result.cart_id == "6"
    assert result.customer_id == "1"


def test_get_cart_by_id_service_invalid(mocker):
    cart_id = "05f11c73e4a4"
    """Checks that the function raises and error when the cart id is not found"""
    mocker.patch("app.services.cart_services.load_all", return_value = mocker_cart_data)
    responseDetail = f"Cart '{cart_id}' not found"
    statusCode = 404
    with pytest.raises(HTTPException) as httpExc:
        get_cart_by_id_service(cart_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail

def test_get_cart_by_id_service_empty(mocker):
    cart_id = ""
    """Checks that the function raises and exception if the cart_id value is empty"""
    mocker.patch("app.services.cart_services.load_all", return_value = mocker_cart_data)
    responseDetail = "cart_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        get_cart_by_id_service(cart_id)

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


expected_data = {
  "cartList": [
    {
      "food_item_id": 1,
      "quantity": 1,
      "price_per_item": 5.99,
      "address_id": "3",
      "cart_item_id": "0120f079-9e09-4c6f-87fa-e767fa79a62b",
      "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
      "subtotal": 5.99
    }
  ],
  "total": 5.99
}

def test_get_cart_items_by_cart_valid(mocker): 
    """Checks that if the cart_id exists the function returns valid data"""
    mocker.patch("app.services.cart_services.load_all_cart_items", return_value = mock_cart_data["cartList"])
    result = get_items_by_cart("e9fffefe-7287-46e4-a433-05f11c73e4a4")
    assert result == expected_data


@pytest.mark.parametrize("cart_id", ["", " "])
def test_get_items_by_cart_empty(cart_id):
    """Checks that if no value or an empty value is requested for cart it raises an exception"""
    responseDetail = "cart_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_cart(cart_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


@pytest.mark.parametrize("cart_id", ["cart_id_not_found"])
def test_get_items_by_cart_id_invalid(cart_id):
    """Checks that if the cart_id does not exists it raises an excpetion"""
    responseDetail = f"Cart '{cart_id}' not found"
    statusCode = 404
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_cart(cart_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


    
mocker_data = { 
    "cart_id": "333", 
    "customer_id": "99" 
    }

expected_create_data = { 
    "cart_id": "333",
    "customer_id": "99"
  }

def test_create_cart_valid(mocker): 
    """Tests creating a new cart with cart_id and customer_id returns expected data"""
    mock_router = mocker.patch("app.services.cart_services.load_all")
    mock_router.return_value = [mocker_data]
    result = create_cart("333", "99")
    assert result == expected_create_data

def test_create_cart_empty(mocker):
    """Tests creating a cart with an empty customer_id raises an exception"""
    mock_router = mocker.patch("app.services.cart_services.load_all")
    mock_router.return_value = [mocker_data]
    responseDetail = "customer_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        create_cart("333", "")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail
  
    


