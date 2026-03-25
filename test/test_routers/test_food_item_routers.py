from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

mock_food_list = [
    {
        "food_item_id": 1,
        "food_name": "bread",
        "restaurant_id": 10,
        "price": 2.50,
        "description": "Soft chunky bread",
        "course": "Main"
    },
    {
        "food_item_id": 2,
        "food_name": "potatoes",
        "restaurant_id": 10,
        "price": 3.00,
        "description": "Sweet and smooth",
        "course": "Side"
    }
]

def test_get_all_food_no_filter():
    """Tests that GET /food-item returns the entire list"""
    with patch("app.routers.food_item.filter_food_items", return_value = mock_food_list):
        response = client.get("/food-items")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["food_name"] == "bread"

def test_get_food_by_id_success():
    """tests that GET /food-items/{id} returns ok 200 for existing item"""
    with patch("app.routers.food_item.get_food_by_id", return_value = mock_food_list[0]):
        response = client.get("/food-items/1")
        assert response.status_code == 200
        assert response.json()["food_item_id"] == 1

def test_post_food_success():
    """tests that POST /food-items creates new item 201 success"""
    new_food_payload = {
        "food_name": "cheeseburger",
        "restaurant_id": 10,
        "price": 12.00,
        "description": "cheesy and chonky",
        "course": "Main"
    }
    mock_reponse = {**new_food_payload, "food_item_id": 3}

    with patch("app.routers.food_item.create_food_item", return_value = mock_reponse):
        response = client.post("/food-items", json = new_food_payload)
        assert response.status_code == 201
        assert response.json()["food_item_id"] == 3

def test_delete_food_success():
    """tests that DELETE /food-items/{id} returns a 204 for successful deletion"""
    with patch("app.routers.food_item.delete_food_item", return_value = True):
        response = client.delete("/food-items/1")
        assert response.status_code == 204

def test_delete_food_not_found():
    """tests that DELETE /food-items/{id} returns 404 if item doesn't exist to delete"""
    with patch("app.routers.food_item.delete_food_item", return_value = False):
        response = client.delete("/food-items/999")
        assert response.status_code == 404