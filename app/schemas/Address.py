from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    """base class for address"""
    street: str  = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str  = Field(min_length=1)
    instructions: Optional[str] = None
    
class AddressCreate(Address):
    """extends base class for creating address"""
    pass


class AddressUpdate(BaseModel):
    """class for updating an address record"""
    street: Optional[str] = Field(default=None, min_length=1)
    city: Optional[str] = Field(default=None, min_length=1)
    postal_code: Optional[str] = Field(default=None, min_length=1)
    instructions: Optional[str] = Field(default=None, min_length=1)

class AddressResponse(Address):
    """response class for address, extends base addres class"""
    address_id: str
    user_id: str
    created_date: datetime
    
