from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.schemas.Role import UserRole

## Base User
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    
class UserResponse(UserBase):
    id: str
    role: UserRole
    created_date: datetime
<<<<<<< HEAD

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1)
    last_name: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=5)

## Customer
=======
    
class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    
>>>>>>> main
class CustomerCreate(UserBase):
    password: str = Field(min_length=5)

class StaffCreate(UserBase):
    password: str = Field(min_length=5)
    