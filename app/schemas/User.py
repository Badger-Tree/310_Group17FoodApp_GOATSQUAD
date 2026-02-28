from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.Address import AddressResponse, Address
from app.schemas.Role import UserRole


## Base User

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    
class UserResponse(UserBase):
    id: str
    role: UserRole
    created_date: datetime
    saved_addresses: Optional[List[AddressResponse]] = None
    
class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    saved_addresses: Optional[List[Address]] = None
## Customer
    
class CustomerCreate(UserBase):
    password: str

## Staff
class StaffCreate(UserBase):
    password: str
    