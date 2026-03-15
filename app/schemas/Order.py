from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from app.schemas.OrderItem import OrderItemCreate, OrderItemResponse # type: ignore
from enum import Enum
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Address import Address
## Base Order


class OrderBase(BaseModel):
    """Base pydantic class or order object"""
    restaurant_id: str = Field(min_length=1)
    customer_id:str = Field(min_length=1)
    delivery_address_id: Optional[str] = Field(default=None)
    delivery_address: Optional[str] = Field(default=None)
    # delivery_address will be an Adress object after merging
    
class OrderCreate(OrderBase):
    """Extension of base order used to structure/orgnaize data used to mkae an order"""
    cart_id: str = Field(min_length=1)

class OrderResponse(OrderBase):
    """Extension of base order class used to send information about an order when requested"""
    order_id: str = Field(min_length=1)
    created_date: datetime
    status: OrderStatus
    total_amount: float 
    delivery_id : Optional[str] = Field(default=None)
    items: List[OrderItemResponse]
    @field_validator("status")
    def convert_status_to_enum(cls, value):
        if isinstance(value, str):
            return OrderStatus(value)
        return value