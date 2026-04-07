from app.schemas.User import UserResponse
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.routers.inventory_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

mock_staff_user = UserResponse.model_construct(
    id="staff1",
    role="STAFF",
    first_name="Test",
    last_name="Staff",
    email="teststaff@example.com"
)

def mock_load_inventory():
    """mocking the data"""
    return [
        {"inventory_id": 1, "food_item_id": 101, "quantity": 10},
        {"inventory_id": 2, "food_item_id": 102, "quantity": 5}
    ]

def mock_save_inventory(*args, **kwargs):
    return None

mock_inventory_response = {
    "inventory_id": 1,
    "food_item_id": 101,
    "quantity": 10
}

def test_get_inventory_success():
    """tests the GET /inventory/{id} and returns 200 ok and correct record"""
    with patch("app.routers.inventory_router.get_user_from_session", return_value=mock_staff_user):
        with patch("app.routers.inventory_router.require_role_service", return_value=None):
            with patch("app.services.inventory_service.get_inventory_by_food_id", return_value=mock_inventory_response):
                response = client.get("/inventory/101", headers={"token": "fake-token"})
        assert response.status_code == 200
        assert response.json() == mock_inventory_response

def test_create_inventory_success():
    """tests POST /inventory/ that it successfully creates a record"""
    new_item = {"food_item_id": 103, "quantity": 20}
    with patch("app.routers.inventory_router.get_user_from_session", return_value=mock_staff_user):
        with patch("app.routers.inventory_router.require_role_service", return_value=None):
            with patch("app.repositories.inventory_repository.load_all", return_value=[]):
                with patch("app.repositories.inventory_repository.save_all", mock_save_inventory):
                    response = client.post("/inventory/", json=new_item, headers={"token": "fake-token"})
            assert response.status_code == 200
            assert response.json()["food_item_id"] == 103
            assert response.json()["quantity"] == 20

def test_update_inventory_success():
    """tests patch /inventory/{id} that it successfully updates quantity"""
    update_data = {"quantity": 15}
    with patch("app.routers.inventory_router.get_user_from_session", return_value=mock_staff_user):
        with patch("app.routers.inventory_router.require_role_service", return_value=None):
            mock_updated = {
                "inventory_id": 1,
                "food_item_id": 101,
                "quantity": 15
            }
        with patch("app.services.inventory_service.update_inventory", return_value=mock_updated):
            response = client.patch("/inventory/101", json=update_data, headers={"token": "fake-token"})
            assert response.status_code == 200
            assert response.json()["quantity"] == 15

