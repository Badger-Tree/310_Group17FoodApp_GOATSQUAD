from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .Address import AddressResponse, Address
#from .Role import Role
## all role fields should be type Role, not str, they are entered as
# str for the purpose of testing until Role branch is merged
from pydantic import Field

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    
class UserResponse(UserBase):
    id: str
    role: List[str]
    created_date: datetime
    
class CustomerBase(UserBase):
    saved_addresses: List[AddressResponse] = Field(default_factory=list)
    
class CustomerCreate(UserBase):
    password: str

class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[List[str]] = None
    saved_addresses: Optional[List[Address]] = None
    
class CustomerResponse(UserResponse, CustomerBase):  
    saved_addresses: List[AddressResponse] = []
    
    
    ###
    
class StaffBase(UserBase):
    pass

class StaffCreate(StaffBase):
    password: str
    
class StaffUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[List[str]] = None

class StaffResponse(StaffBase, UserResponse):
    pass
