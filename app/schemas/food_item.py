from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

#parent class
class FoodItemBase(BaseModel):
    food_name: str
    restaurant_id: int
    price: Decimal = Field(max_digits=10, decimal_places=2)
    description: str
    course: str

class FoodItemCreate(FoodItemBase):
    pass #inherits from FoodItemBase; adds nothing new

class FoodItemUpdate(BaseModel):
    food_name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    course: Optional[str] = None

class FoodItem(FoodItemBase):
    food_item_id: int

    class Config:
        #to let Pydantic read data from db objs (ORMs)
        from_attributes = True 