from fastapi import FastAPI
from unittest.mock import patch
from app.routers.cart_router import router
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app)

class MockUser:
    def __init__(self, id):
        self.id = id

class Token:
    def __init__(self, token): 
        self.token = token

def test_cart_add_success(mocker):
    """Tests that adding an item to the cart is successful"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}

    mock_user = MockUser(id="2")
    mock_token = Token(token = "RANDOMTOKEN")

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.Token", return_value=mock_token)
    response = client.post(
        "/cart/food_item/add",
        json=mock_cart_create,
        headers={"token": "RANDOMTOKEN"}
    )

    assert response.status_code == 201


def test_cart_wrong_token(mocker):
    """Tests that adding an item to the cart with the wrong token raises an error because customer_id does not exist"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}

    mock_user = MockUser(id="2")
    mock_token = Token(token = "RANDOMTOKEN")

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.Token", return_value=mock_token)
    response = client.post(
        "/cart/food_item/add",
        json=mock_cart_create,
        headers={"token": "invalidtoken"}
        )

    assert response.status_code == 404

def test_cart_invalid(mocker):
    """Tests creating a cart with invalid data raises an error"""
    mock_cart_create = {"food_item_id": 2, "quantity": "invalid"}

    mock_user = MockUser(id="2")

    mock_response = {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [],
        "total": 0.0
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.add_to_cart", return_value=mock_response)

    response = client.post("/cart/food_item/add",json=mock_cart_create,headers={"token": "fake-token"})

    assert response.status_code == 422


def test_remove_cart_item_success(mocker):
    """Tests that deleting an item from the cart is successful"""

    mock_user = MockUser(id="2")
    mock_token = Token(token = "RANDOMTOKEN")

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.Token", return_value=mock_token)
    response = client.delete("/cart/food_item/remove",params={"cart_item_id": "FJSKJAHJ"},headers={"token": "RANDOMTOKEN"}
        )

    assert response.status_code == 201

def test_remove_cart_item_wrong_token(mocker):
    """Tests that deleting an item with the wrong token raises an error"""

    mock_user = MockUser(id="2")
    mock_token = Token(token = "RANDOMTOKEN")

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.Token", return_value=mock_token)
    response = client.delete("/cart/food_item/remove",params={"cart_item_id": "FJSKJAHJ"},headers={"token": "RANDOMTOKEN"}
        )

    assert response.status_code == 404


def test_remove_cart_item_invalid(mocker):
    """Tests removing a cart with invalid cart_item_id raises an error"""

    mock_user = MockUser(id="2")

    mock_response = {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [],
        "total": 0.0
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.routers.cart_router.add_to_cart", return_value=mock_response)

    response = client.delete("/cart/food_item/remove",params={"cart_item_id": "FJSKJAHJ"}, headers={"token": "RANDOMTOKEN"})

    assert response.status_code == 404