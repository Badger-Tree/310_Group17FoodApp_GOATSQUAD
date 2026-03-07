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

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1)
    last_name: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=5)


## Customer
class CustomerCreate(UserBase):
    password: str = Field(min_length=5)

## Staff
class StaffCreate(UserBase):
    password: str = Field(min_length=5)
    