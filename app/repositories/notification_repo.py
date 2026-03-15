from pathlib import Path
import csv
from app.schemas.notification import Notification

DATA_PATH = Path("app/data/notification.csv")
FIELDNAMES = ["notification_id", "recipient_user_id", "notification_type", "message", "status"]

def load_all():
    """Loads all notifications from the CSV file and returns a list of Notification objects."""
    if not DATA_PATH.exists():
        return []

    items = []
    with open(DATA_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(Notification(**row))
    return items

def save_all(items):
    """Saves a list of Notification objects to the CSV file."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for item in items:
        if isinstance(item, Notification):
            rows.append(item.model_dump())
        else:
            rows.append(item)

    with open(DATA_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)