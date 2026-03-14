import pytest 
from pydantic import ValidationError
from uuid import uuid4
from app.schemas.notification import NotificationCreate, NotificationType, NotificationStatus

def test_notification_create_success():
    """Tests that NotificationCreate instantiates with valid input"""
    user_uuid = str(uuid4())
    input_data = {
        "recipient_user_id": user_uuid,
        "notification_type": "order",
        "message": "Your order has been placed successfully!",
        "status": "sent"
    }
    result = NotificationCreate(**input_data)
    assert result.recipient_user_id == user_uuid
    assert result.notification_type == NotificationType.ORDER.value
    assert result.status == NotificationStatus.SENT.value

def test_notification_default_status():
    """Tests that NotificationCreate defaults status to SENT if not provided"""
    user_uuid = str(uuid4())
    input_data = {
        "recipient_user_id": user_uuid,
        "notification_type": "order",
        "message": "Testing default status"
    }
    result = NotificationCreate(**input_data)
    assert result.status == NotificationStatus.SENT.value

def test_notification_enum_validation():
    """Tests that only valid NotificationTypes are allowed"""
    input_data = {
        "recipient_user_id": str(uuid4()),
        "notification_type": "invalid_type",
        "message": "This should fail",
        "status": "sent"
    }
    with pytest.raises(ValidationError):
        NotificationCreate(**input_data)

def test_notification_missing_fields():
    """Tests that missing required fields will raise a ValidationError."""
    input_data = {
        "notification_type":"delivery",
        "message": "Your order is out for delivery!",
        "status": "sent"
    }
    with pytest.raises(ValidationError):
        NotificationCreate(**input_data)
