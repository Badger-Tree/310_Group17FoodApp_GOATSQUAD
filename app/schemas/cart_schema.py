from pydantic import BaseModel, Field, PositiveInt
from typing import List, Optional
from app.schemas.cart_item_schema import CartItemResponse

class CartBase(BaseModel):
    customer_id: str
    cart_id: str
    cart_items: List[CartItemResponse] = Field(default_factory=list)
    total: Optional[float] = 0

class CartResponse(CartBase): 
    pass

class CartCreate(BaseModel):
    food_item_id: int
    quantity: PositiveInt


class CartUpdate(CartCreate): 
    pass
