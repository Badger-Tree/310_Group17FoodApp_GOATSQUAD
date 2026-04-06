from pydantic import BaseModel
from pydantic import PositiveInt


class TrackRestaurantBase(BaseModel):
    restaurant_id: PositiveInt
    count: PositiveInt

class TrackRestaurantResponse(TrackRestaurantBase): 
    pass

"""

class TrackFoodBase(BaseModel):
    food_item_id: str
    count: int

class TrackFoodResponse(TrackFoodBase): 
    pass

"""