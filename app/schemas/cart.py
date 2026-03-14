from pydantic import BaseModel
from typing import Optional, List


class CartBase(BaseModel):
        food_item_id: int
        quantity: int
        price_per_item: Optional[float] = None

class CartResponse(CartBase):
        cart_item_id: str
        cart_id: str
        subtotal: Optional[float] = None

class ListCartResponse(BaseModel): 
        cartList: List[CartResponse]
        total: Optional[float] = None