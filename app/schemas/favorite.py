from pydantic import BaseModel
from enum import Enum

class FavoriteType(str, Enum):
    RESTAURANT = "RESTAURANT"
    ORDER = "ORDER"

    
class FavoriteBase(BaseModel):
    target_id: str
    favorite_type: FavoriteType

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    user_id: str