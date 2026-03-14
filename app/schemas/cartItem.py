from pydantic import BaseModel, PositiveInt
from typing import Optional
from decimal import Decimal

class CartItemBase(BaseModel):
        food_item_id: int 
        quantity: PositiveInt

class CartItemResponse(CartItemBase):
        address_id: str
        cart_item_id: str 
        cart_id: str 
        price_per_item: Optional[float] = None
        subtotal: float

class CartItemAdd(CartItemBase): 
        customer_id: str

class CartItemUpdate(BaseModel):
        quantity: PositiveInt
        price_per_item: Decimal