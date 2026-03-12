from enum import Enum

class OrderStatus(str, Enum):
    """enum class used to restruct values for an order status"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CANCELED = "CANCELED"
    IN_PREPARATION = "IN_PREPARATION",
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    COMPLETED = "COMPLETED"