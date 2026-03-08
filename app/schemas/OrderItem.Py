from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    """base pydantic class for an item in an order"""
    food_item_id: str = Field(min_length=1)
    quantity:int = Field(...,gt=0) 
    price_per_item: float = Field(...,gt=0)

class OrderItemCreate(OrderItemBase):
    """Extension of base order used to structure/orgnaize data used to create an item in an order"""
    pass
    
class OrderItemResponse(OrderItemBase):
    """Extension of base order class used to send information about an order item when requested"""
    order_item_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)