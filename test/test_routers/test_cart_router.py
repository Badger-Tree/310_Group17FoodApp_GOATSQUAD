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

def test_cart_add_success():
    """Tests that adding an item to the cart is successful"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}

    mock_user = MockUser(id="2")
    

    mock_response = {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [],
        "total": 0.0
    }

    with patch("app.routers.cart_router.get_user_from_session", return_value=mock_user):
            with patch("app.routers.cart_router.add_to_cart", return_value=mock_response):
                response = client.post(
                    "/cart/food_item/add",
                    json=mock_cart_create,
                    headers={"token": "fake-token"}
            )

            assert response.status_code == 201


def test_cart_wrong_token():
    """Tests that adding an item to the cart with the wrong token raises an error because customer_id does not exist"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}

    mock_user = MockUser(id="2")
    mock_token = Token(token = "RANDOMTOKEN")

    with patch("app.routers.cart_router.get_user_from_session", return_value=mock_user):
        with patch("app.routers.cart_router.Token", return_value=mock_token):
                response = client.post(
                    "/cart/food_item/add",
                    json=mock_cart_create,
                    headers={"token": "invalidtoken"}
            )

        assert response.status_code == 404

def test_cart_invalid():
    """Tests creating a cart with invalid data raises an error"""
    mock_cart_create = {"food_item_id": 2, "quantity": "invalid"}

    mock_user = MockUser(id="2")

    mock_response = {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [],
        "total": 0.0
    }

    with patch("app.routers.cart_router.get_user_from_session", return_value=mock_user):
        with patch("app.routers.cart_router.add_to_cart", return_value=mock_response):

            response = client.post("/cart/food_item/add",json=mock_cart_create,headers={"token": "fake-token"}
            )

            assert response.status_code == 422

