
from pydantic import BaseModel, Field, PositiveInt
from decimal import Decimal
from typing import Optional

class CartItemBase(BaseModel):
        food_item_id: int
        quantity: PositiveInt
        price_per_item: Decimal = Field(max_digits=10, decimal_places=2)


class CartItemResponse(CartItemBase):
        cart_item_id: str
        cart_id: str
        subtotal: Optional[Decimal] = None

class CartItemUpdate(BaseModel):
     quantity: PositiveInt
     price_per_item: Decimal