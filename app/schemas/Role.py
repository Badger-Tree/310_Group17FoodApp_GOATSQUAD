
from enum import Enum

class UserRole(str, Enum):
    """class used to define a user's role in the system"""
    CUSTOMER="CUSTOMER"
    STAFF = "STAFF"
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    COURIER = "COURIER"



