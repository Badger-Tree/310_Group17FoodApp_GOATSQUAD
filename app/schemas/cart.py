from pydantic import BaseModel, PositiveInt, PositiveFloat
from typing import Optional, List

class CartBase(BaseModel):
        cart_id: str
        customer_id: Optional[str] = None

class CartResponse(CartBase):
        cart_item_id: str
        food_item_id: int
        quantity: PositiveInt
        price_per_item: PositiveFloat
        subtotal: float

class ListCartResponse(BaseModel): 
        cartList: List[CartResponse]
        total: Optional[float] = None
