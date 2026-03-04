from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from app.schemas.OrderItem import OrderItemCreate, OrderItemResponse # type: ignore
from enum import Enum
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Address import Address
## Base Order

class OrderBase(BaseModel):
    restaurant_id: str
    customer_id:str
    delivery_address: Address
    
class OrderCreate(OrderBase):
    cart_id: str
    items: List[OrderItemCreate] = Field(...,min_length=1)
    
class OrderResponse(OrderBase):
    order_id: str
    created_date: datetime
    status: OrderStatus
    total_amount: float
    delivery_id: str
    items: List[OrderItemResponse]
    
    @validator("status", pre=True)
    def convert_status_to_enum(cls, value):
        if isinstance(value, str):
            return OrderStatus(value)
        return value