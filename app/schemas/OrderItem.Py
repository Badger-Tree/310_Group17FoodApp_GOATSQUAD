from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    food_item_id: str
    quantity:int
    price_per_item: float
    
class OrderItemCreate(BaseModel):
    pass
    
class OrderItemResponse(OrderItemBase):
    order_item_id: str
    order_id: str