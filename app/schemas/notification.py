from enum import Enum
from pydantic import BaseModel

class NotificationType(str, Enum):
    ORDER = "order"
    DELIVERY = "delivery"
    PAYMENT = "payment"

class NotificationStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    PENDING = "pending"
    FAILED = "failed"

class NotificationBase(BaseModel):
    recipient_user_id: str
    notification_type: NotificationType
    message: str
    status: NotificationStatus = NotificationStatus.SENT

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: int