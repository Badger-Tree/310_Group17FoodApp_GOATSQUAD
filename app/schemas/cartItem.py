from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    food_item_id: str
    quantity: int
    price_per_item: Optional[float] = None

class CartItemResponse(CartItemBase): 
    cart_item_id: str
    cart_id: str
    subtotal: Optional[float] = None

class CartItemAdd(CartItemBase):
    customer_id: str

class CartItemUpdate(BaseModel):
     quantity: Optional[int] = None
     price_per_item: Optional[float] = None