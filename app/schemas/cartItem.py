from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class CartItemBase(BaseModel):
        food_item_id: int
        quantity: int
        price_per_item: Optional[float] = None


class CartItemResponse(CartItemBase):
        cart_item_id: str
        cart_id: str
        subtotal: Optional[float] = None