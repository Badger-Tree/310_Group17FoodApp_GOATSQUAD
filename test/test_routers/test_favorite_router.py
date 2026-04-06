import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.User import UserResponse

client = TestClient(app)

mock_user = UserResponse(id="user1", email="user1@example.com", first_name="John", last_name="Doe", role="CUSTOMER", created_date="2024-01-01T00:00:00Z")

def test_list_my_favorites_success():
    """tests GET /favorites/me endpoint with valid token and existing favorites"""
    with patch("app.routers.favorite_router.get_user_from_session", return_value=mock_user):
        with patch("app.services.favorite_service.get_favorites", return_value=[{"name": "Pizza place"}]):
            response = client.get("/favorites/me", headers={"token": "fake-valid-token"})

            assert response.status_code == 200
            assert response.json() == [{"name": "Pizza place"}]

def test_add_to_favorites_success():
    """tests POST /favorites/{fav_type}/{target_id} endpoint with valid token and new favorite"""
    with patch("app.routers.favorite_router.get_user_from_session", return_value=mock_user):
        with patch("app.services.favorite_service.add_favorite", return_value={"user_id": "user1", "target_id": "rest1", "favorite_type": "RESTAURANT"}):
            response = client.post("/favorites/RESTAURANT/rest1", headers={"token": "fake-valid-token"})

            assert response.status_code == 201
            assert response.json() == {"user_id": "user1", "target_id": "rest1", "favorite_type": "RESTAURANT"}

def test_remove_favorite_success():
    """tests DELETE /favorites/{fav_type}/{target_id} endpoint with valid token and existing favorite"""
    with patch("app.routers.favorite_router.get_user_from_session", return_value=mock_user):
        with patch("app.services.favorite_service.delete_favorite", return_value=True):
            response = client.delete("/favorites/RESTAURANT/rest1", headers={"token": "fake-valid-token"})

            assert response.status_code == 204

