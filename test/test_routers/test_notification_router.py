import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_notify_order_placed_endpoint(monkeypatch):
    """Tests the post /notifications/order-placed endpoint to ensure it returns a success message."""
    notifications_sent = []
    def mock_notify_order_placed(customer_id, restaurant_id, order_id):
        notifications_sent.append((customer_id, restaurant_id, order_id))

    monkeypatch.setattr("app.routers.notification_router.notify_order_placed", mock_notify_order_placed)
    response = client.post("/notifications/order-placed", params={"customer_id": "customer123", "restaurant_id": "restaurant456", "order_id": "order789"})

    assert response.status_code == 201
    assert response.json() == {"status": "success", "message": "Notifications sent for order order789."}
    assert notifications_sent == [("customer123", "restaurant456", "order789")]

def test_get_notifications_by_user(monkeypatch):
    """Tests the get /notifications/user/{user_id} endpoint."""
    test_user = "user123"
    def mock_get_user_inbox(user_id):
        return [
            {
                "notification_id": 1,
                "recipient_user_id": user_id,
                "notification_type": "order",
                "message": "test",
                "status": "pending"
            }
        ]
    monkeypatch.setattr("app.routers.notification_router.get_user_inbox", mock_get_user_inbox)
    response = client.get(f"/notifications/user/{test_user}")
    assert response.status_code == 200
    assert response.json()[0]["recipient_user_id"] == test_user
    assert response.json()[0]["notification_type"] == "order"
    assert response.json()[0]["message"] == "test"
    assert response.json()[0]["status"] == "pending"
    assert response.json()[0]["notification_id"] == 1

def test_get_notifications_empty_inbox(monkeypatch):
    """Tests that a user with no notifications receives an empty list."""
    def mock_get_user_inbox(user_id):
        return []
    monkeypatch.setattr("app.routers.notification_router.get_user_inbox", mock_get_user_inbox)
    response = client.get("/notifications/user/user_with_no_notifications")

    assert response.status_code == 200
    assert response.json() == []