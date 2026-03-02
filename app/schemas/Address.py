from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Address(BaseModel):
    street: str 
    city: str
    postal_code: str 
    instructions: str
    
class AddressCreate(Address):
    user_id: str

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    instructions: Optional[str] = None

class AddressResponse(Address):
    address_id: str
    user_id: str
    created_date: datetime
    
