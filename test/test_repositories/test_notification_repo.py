import pytest, csv
from app.repositories import notification_repo
from app.repositories.notification_repo import load_all, save_all
from app.schemas.notification import Notification, NotificationType, NotificationStatus

def test_load_all_success(monkeypatch, tmp_path):
    """Tests that load_all() returns a list of Notification objects when the csv exists and has data."""
    mock_path = tmp_path / "notification.csv"

    mock_path.write_text(
        "notification_id,recipient_user_id,notification_type,message,status\n"
        "1,user-123,order,Your order is on the way,pending\n"
        "2,user-456,delivery,Your order has been delivered!,delivered\n"
    )

    monkeypatch.setattr("app.repositories.notification_repo.DATA_PATH", mock_path)

    result = load_all()

    assert len(result) == 2
    assert result[0].notification_id == 1
    assert result[1].recipient_user_id == "user-456"
    assert result[1].status == NotificationStatus.DELIVERED
    assert isinstance(result[0], Notification)

def test_load_all_file_not_exist(monkeypatch, tmp_path):
    """Tests that load_all() returns an empty list if file doesn't exist."""
    mock_path = tmp_path / "notification.csv"
    monkeypatch.setattr("app.repositories.notification_repo.DATA_PATH", mock_path)

    result = load_all()
    assert result == []

def test_save_all_success(monkeypatch, tmp_path):
    """Tests that save_all() overwrites csv with new input data."""
    mock_path = tmp_path / "notification.csv"
    mock_path.write_text(
        "notification_id,recipient_user_id,notification_type,message,status\n"
        "99,old-user,order,old message,sent\n"
    )

    monkeypatch.setattr("app.repositories.notification_repo.DATA_PATH", mock_path)

    input_data = [
        Notification(
            notification_id=1,
            recipient_user_id="new-user",
            notification_type=NotificationType.ORDER,
            message="New message",
            status=NotificationStatus.PENDING
        )
    ]

    save_all(input_data)

    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["notification_id"] == "1"
    assert rows[0]["recipient_user_id"] == "new-user"
    assert rows[0]["notification_type"] == NotificationType.ORDER.value
    assert rows[0]["message"] == "New message"
    assert rows[0]["status"] == NotificationStatus.PENDING.value

def test_create_notification_empty_file(monkeypatch, tmp_path):
    """Tests that the first notification created gets an id of 1."""
    mock_path = tmp_path / "notification.csv"
    monkeypatch.setattr("app.repositories.notification_repo.DATA_PATH", mock_path)

    new_data = {
        "recipient_user_id": "user-123",
        "notification_type": "order",
        "message": "testing for first notification id creation",
        "status": "pending"
    }

    result = notification_repo.create_notification(new_data)

    assert result["notification_id"] == 1
    assert result["message"] == "testing for first notification id creation"

    notifications = notification_repo.load_all()
    assert len(notifications) == 1
    assert notifications[0].notification_id == 1

def test_create_notification_increments_id(monkeypatch, tmp_path):
    """tests that new notifications increment based on existing max id."""
    mock_path = tmp_path / "notification.csv"
    mock_path.write_text(
        "notification_id,recipient_user_id,notification_type,message,status\n"
        "10,user-123,order,Old message,sent\n"
    )
    monkeypatch.setattr("app.repositories.notification_repo.DATA_PATH", mock_path)

    new_data = {
        "recipient_user_id": "user-456",
        "notification_type": "delivery",
        "message": "New message",
        "status": "pending"
    }

    result = notification_repo.create_notification(new_data)

    assert result["notification_id"] == 11
    all_records = notification_repo.load_all()
    assert len(all_records) == 2