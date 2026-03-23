from enum import Enum

class OrderStatus(str, Enum):
    """enum class used to restruct values for an order status"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    CANCELED = "CANCELED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    COMPLETED = "COMPLETED"