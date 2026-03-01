from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.OrderItem import OrderItemResponse # type: ignore
# from app.schemas.Address import AddressResponse, Address
# from app.schemas.Role import UserRole


## Base Order

class OrderBase(BaseModel):
    restaurant_id: str
    customer_id:str
class OrderCreate(BaseModel):
    cart_id: str
class OrderResponse(OrderBase):
    order_id: str
    created_date: datetime
    status: str
    total_amount: float
    delivery_id: str
    items: List[OrderItemResponse]