import pytest
from app.services import notification_service

def test_notify_order_placed(monkeypatch):
    """Tests that notify_order_placed creates notifications for both customer and restaurant."""
    created_notifications = []

    def mock_create_notification(notification_data):
        """Mocks the create_notification function to capture created notifications."""
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_order_placed("customer123", "restaurant456", "order789")

    assert len(created_notifications) == 2

    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "order"
    assert created_notifications[0]["status"] =="pending"

    assert created_notifications[1]["recipient_user_id"] == "restaurant456"
    assert created_notifications[1]["notification_type"] == "order"
    assert created_notifications[1]["status"] == "pending"

def test_notify_order_ready_for_pickup(monkeypatch):
    """Tests that courier is notified when order is ready for pickup."""
    created_notifications = []

    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_order_ready_for_pickup("courier123", "order789")

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "courier123"
    assert created_notifications[0]["notification_type"] == "delivery"
    assert created_notifications[0]["status"] == "pending"

def test_notify_out_for_delivery(monkeypatch):
    """Tests that customer is notified when order is out for delivery."""
    created_notifications = []
    
    def mock_create_notification(notification_data):
        """Mocks the create_notification function to capture created notifications."""
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_out_for_delivery("customer123", "order789")

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "delivery"
    assert created_notifications[0]["status"] == "pending"

def test_notify_order_delivered(monkeypatch):
    """Tests that customer is notified when order is delivered."""
    created_notifications = []
    
    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_order_delivered("customer123", "order789")

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "delivery"
    assert created_notifications[0]["status"] == "delivered"

def test_notify_payment_status(monkeypatch):
    """Tests notification for a successful payment"""
    created_notifications = []

    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)
    notification_service.notify_payment_status("customer123", "order789", is_success=True)

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "payment"
    assert created_notifications[0]["status"] == "pending"

def test_notify_payment_status_failed(monkeypatch):
    """Tests notification for a failed payment"""
    created_notifications = []

    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)
    notification_service.notify_payment_status("customer123", "order789", is_success=False)

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "payment"
    assert created_notifications[0]["status"] == "failed"

def test_notify_order_status_update_approved(monkeypatch):
    """Tests that customer is notified when order is approved by restaurant."""
    created_notifications = []
    
    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_order_status_update("customer123", "order789", is_approved=True)

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "order"
    assert created_notifications[0]["status"] == "pending"

def test_notify_order_status_update_rejected(monkeypatch):
    """Tests that customer is notified when order is rejected by restaurant."""
    created_notifications = []
    
    def mock_create_notification(notification_data):
        created_notifications.append(notification_data)
        return notification_data
    
    monkeypatch.setattr("app.repositories.notification_repo.create_notification", mock_create_notification)

    notification_service.notify_order_status_update("customer123", "order789", is_approved=False)

    assert len(created_notifications) == 1
    assert created_notifications[0]["recipient_user_id"] == "customer123"
    assert created_notifications[0]["notification_type"] == "order"
    assert created_notifications[0]["status"] == "failed"