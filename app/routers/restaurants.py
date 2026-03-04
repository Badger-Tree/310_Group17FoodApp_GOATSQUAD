from fastapi import APIRouter, status
from typing import List

from app.schemas.Restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.services.restaurant_service import (
    create_restaurant_service,
    update_restaurant_service,
    activate_restaurant_service,
    deactivate_restaurant_service,
    delete_restaurant_service,
    get_restaurant_by_name_service,
    get_restaurant_by_cuisine_service,
    sort_restaurants_by_name_service
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

"""This is where I will keep the endpoints"""

#Create restaurant
@router.post("/", response_model = RestaurantResponse)
def create_restaurant(payload: RestaurantCreate):
    return create_restaurant_service(payload)

#Update Restaurant
@router.put("/{restaurant_id}", response_model = RestaurantResponse)
def update_restaurant(restaurant_id: int, payload: RestaurantUpdate):
    return update_restaurant_service(restaurant_id, payload)

#Activate restaurant
@router.post("/activate/{restaurant_id}", response_model = RestaurantResponse)
def activate_restaurant(restaurant_id: int):
    return activate_restaurant_service(restaurant_id)

#Deactivate restaurant
@router.post("/deactivate/{restaurant_id}", response_model = RestaurantResponse)
def deactivate_restaurant(restaurant_id: int):
    return deactivate_restaurant_service(restaurant_id)

#Delete restaurant
@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    delete_restaurant_service(restaurant_id)
    return {"message": f"Restaurant with id {restaurant_id} has been deleted."}

#Get restaurant by name
@router.get("/search/name/{search_name}", response_model = List[RestaurantResponse])
def get_restaurant_by_name(search_name: str):
    return get_restaurant_by_name_service(search_name)

#Get restaurant by cuisine
@router.get("/search/cuisine/{search_cuisine}", response_model = List[RestaurantResponse])
def get_restaurant_by_cuisine(search_cuisine: str):
    return get_restaurnat_by_cuisine_service(search_cuisine)

#Sort restaurants by name
@router.get("/sort/name", response_model = List[RestaurantResponse])
def sort_restaurants_by_name():
    return sort_restaurants_by_name_service()
