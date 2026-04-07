from pydantic import BaseModel
from pydantic import PositiveInt

class TrackFoodBase(BaseModel):
    food_item_id: PositiveInt
    order_count: PositiveInt

class TrackFoodResponse(TrackFoodBase): 
    pass