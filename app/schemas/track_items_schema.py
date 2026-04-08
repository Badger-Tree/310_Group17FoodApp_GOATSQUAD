from pydantic import BaseModel
from pydantic import PositiveInt
from typing import Optional


class TrackRestaurantBase(BaseModel):
    restaurant_id: PositiveInt
    order_count: PositiveInt

class TrackRestaurantResponse(BaseModel): 
    restaurant_name: Optional[str]
    order_count: PositiveInt

