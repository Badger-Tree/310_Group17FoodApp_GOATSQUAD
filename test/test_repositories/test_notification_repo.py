import pytest, csv
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
