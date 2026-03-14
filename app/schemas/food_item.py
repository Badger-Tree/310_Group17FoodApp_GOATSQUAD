from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class FoodItemBase(BaseModel):
    food_name: str
    restaurant_id: int
    price: Decimal = Field(max_digits=10, decimal_places=2)
    description: str
    course: str

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemUpdate(BaseModel):
    food_name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    course: Optional[str] = None

class FoodItem(FoodItemBase):
    food_item_id: int
