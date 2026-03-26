from pydantic import BaseModel
from datetime import time
from typing import Optional

""" This is the base model for restaurant"""
class RestaurantBase(BaseModel):
    restaurant_name: str
    cuisine: str
    address: str
    open_hour: time
    closed_hour: time

"""User creates a restaurant with this"""
class RestaurantCreate(RestaurantBase):
    pass

"""User can update any of the restaurant information except for the ids"""
class RestaurantUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    cuisine: Optional[str] = None
    address: Optional[str] = None
    open_hour: Optional[time] = None
    closed_hour: Optional[time] = None
    restaurant_status: Optional[str] = None

"""When a user creates a restaurant, the system will return with a restaurant id, the owner id given earlier    
    and the restaurant status"""
class RestaurantResponse(RestaurantBase):
    restaurant_id: int
    owner_id: str
    restaurant_status: str