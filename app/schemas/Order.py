from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from app.schemas.OrderItem import OrderItemResponse # type: ignore
from enum import Enum
from app.schemas.OrderStatus import OrderStatus

## Base Order

class OrderBase(BaseModel):
    restaurant_id: str
    customer_id:str
class OrderCreate(BaseModel):
    cart_id: str
    items: List[OrderItemResponse]
    customer_id:str
    restaurant_id: str
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