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
    """Successfully adds a cart item to a cart with valid customer id, food item id, and quantity"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}
    mock_user = MockUser(id="2")
    mock_cart = [{
        "customer_id": "2",
        "cart_id": "RANDOMCART",
        "cart_items": [],
        "total": 0.0
    }]
    mock_food = [{"food_item_id": 2, "price": 10.0}]

    def mock_add_cart_item(cart_add, price):
        return {
            "food_item_id": cart_add.food_item_id,
            "quantity": cart_add.quantity,
            "subtotal": cart_add.quantity * price
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_food_items", return_value= mock_food)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.add_cart_item", side_effect=mock_add_cart_item)

    response = client.post(
        "/cart/food_item/add",
        json=mock_cart_create,
        headers={"token": "RANDOMTOKEN"}
    )

    assert response.status_code == 201 


def test_cart_wrong_customer(mocker):
    """Tests that adding an item to the cart with the wrong token raises an error because customer_id does not exist"""
    mock_cart_create = {"food_item_id": 2, "quantity": 3}
    mock_user = MockUser(id="2")
    mock_cart = [{
        "customer_id": "5",
        "cart_id": "RANDOMCART",
        "cart_items": [],
        "total": 0.0
    }]
    mock_food = [{"food_item_id": 2, "price": 10.0}]

    def mock_add_cart_item(cart_add, price):
        return {
            "food_item_id": cart_add.food_item_id,
            "quantity": cart_add.quantity,
            "subtotal": cart_add.quantity * price
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_food_items", return_value= mock_food)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.add_cart_item", side_effect=mock_add_cart_item)

    response = client.post(
        "/cart/food_item/add",
        json=mock_cart_create,
        headers={"token": "INVALIDTOKEN"}
    )

    assert response.status_code == 404


def test_cart_invalid(mocker):
    """Tests creating a cart with invalid data raises an error"""
    mock_cart_create = {"food_item_id": 2, "quantity": "inavlid"}
    mock_user = MockUser(id="2")
    mock_cart = [{
        "customer_id": "2",
        "cart_id": "RANDOMCART",
        "cart_items": [],
        "total": 0.0
    }]
    mock_food = [{"food_item_id": 2, "price": 10.0}]

    def mock_add_cart_item(cart_add, price):
        return {
            "food_item_id": cart_add.food_item_id,
            "quantity": cart_add.quantity,
            "subtotal": cart_add.quantity * price
    }

    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_food_items", return_value= mock_food)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.add_cart_item", side_effect=mock_add_cart_item)

    response = client.post(
        "/cart/food_item/add",
        json=mock_cart_create,
        headers={"token": "RANDOMTOKEN"}
    )

    assert response.status_code == 422



def test_remove_first_cart_item_success(mocker):
    """Tests that deleting the first item from the cart is successful"""
    mock_cart_item_id = "01KM8SQ4JB61NVWKSM2AVSFN3C"
    mock_user = MockUser(id="2")
    mock_cart = [
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
    
    mock_cart_deleted= [
    {
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [

             {
                "cart_item_id": "61NVWKSM2AVSFDFKSLAJA",
                "food_item_id": 1,
                "quantity": 1,
                "price_per_item": 15.5,
                "subtotal": 15.5
            }
        ],
        "total": 15.5
    }
]

    def mock_delete_cart_item():
        return mock_cart_deleted


    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.delete_cart_item", side_effect=mock_delete_cart_item)

    response = client.delete(
        "/cart/food_item/remove",
        params={"cart_item_id": mock_cart_item_id},
        headers={"token": "RANDOMTOKEN"}
    )

    assert response.status_code == 201


def test_remove_last_cart_item_success(mocker):
    """Tests that deleting the last item from the cart is successful"""
    mock_cart_item_id = "61NVWKSM2AVSFDFKSLAJA"
    mock_user = MockUser(id="2")
    mock_cart = [
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
    
    mock_cart_deleted= [
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

    def mock_delete_cart_item():
        return mock_cart_deleted


    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.delete_cart_item", side_effect=mock_delete_cart_item)

    response = client.delete(
        "/cart/food_item/remove",
        params={"cart_item_id": mock_cart_item_id},
        headers={"token": "RANDOMTOKEN"}
    )

    assert response.status_code == 201


def test_remove_wrong_customer_id(mocker):
    """Tests that deleting an item from the cart with incorrect customer is insuccessful"""
    mock_cart_item_id = "61NVWKSM2AVSFDFKSLAJA"
    mock_user = MockUser(id="5")
    mock_cart = [
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
    
    mock_cart_deleted= [
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

    def mock_delete_cart_item():
        return mock_cart_deleted


    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.delete_cart_item", side_effect=mock_delete_cart_item)

    response = client.delete(
        "/cart/food_item/remove",
        params={"cart_item_id": mock_cart_item_id},
        headers={"token": "WRONGTOKEN"}
    )

    assert response.status_code == 404


def test_remove_wrong_cart_item_id(mocker):
    """Tests that trying to delete an item with wrong cart item id riases error"""
    mock_cart_item_id = "KSM2AVSFDFKS"
    mock_user = MockUser(id="5")
    mock_cart = [
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
    
    mock_cart_deleted= [
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

    def mock_delete_cart_item():
        return mock_cart_deleted


    mocker.patch("app.routers.cart_router.get_user_from_session", return_value=mock_user)
    mocker.patch("app.services.cart_service.load_all_carts", return_value=mock_cart)
    mocker.patch("app.services.cart_service.save_cart", return_value=None)
    mocker.patch("app.services.cart_item_service.delete_cart_item", side_effect=mock_delete_cart_item)

    response = client.delete(
        "/cart/food_item/remove",
        params={"cart_item_id": mock_cart_item_id},
        headers={"token": "TOKEN"}
    )

    assert response.status_code == 404