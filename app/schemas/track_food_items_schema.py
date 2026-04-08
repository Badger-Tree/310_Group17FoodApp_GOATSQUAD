from pydantic import BaseModel, Field, PositiveInt
from typing import Optional

class TrackFoodBase(BaseModel):
    food_item_id: PositiveInt
    order_count: int = Field(..., ge=0)

class TrackFoodResponse(TrackFoodBase): 
    food_name: Optional[str]
    