from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    food_item_id: str
    quantity:int = Field(...,gt=0)
    price_per_item: float = Field(...,gt=0)

    
class OrderItemCreate(OrderItemBase):
    pass
    
class OrderItemResponse(OrderItemBase):
    order_item_id: str  
    order_id: str

