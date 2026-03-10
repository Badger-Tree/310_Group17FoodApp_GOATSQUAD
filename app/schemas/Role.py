
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER="CUSTOMER"
    STAFF = "STAFF"
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    COURIER = "COURIER"



