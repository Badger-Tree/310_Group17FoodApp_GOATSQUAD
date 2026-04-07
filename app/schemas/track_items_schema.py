from pydantic import BaseModel
from pydantic import PositiveInt


class TrackRestaurantBase(BaseModel):
    restaurant_id: PositiveInt
    order_count: PositiveInt

class TrackRestaurantResponse(BaseModel): 
    restaurant_name: str
    order_count: PositiveInt

