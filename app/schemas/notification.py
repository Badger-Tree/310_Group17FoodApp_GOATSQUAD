from enum import Enum
from pydantic import BaseModel

class NotificationType(str, Enum):
    ORDER = "order"
    DELIVERY = "delivery"
    PAYMENT = "payment"

class NotificationBase(BaseModel):
    recipient_user_id: str
    notification_type: NotificationType
    message: str
    status: str = "sent"

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: int