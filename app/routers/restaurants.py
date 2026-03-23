from fastapi import APIRouter, status, Header
from typing import List
from app.services.authorization_service import require_role_service
from app.services.session_manager_service import get_user_from_session,validate_token_service
from app.schemas.Token import Token
from app.schemas.Role import UserRole
from enum import Enum
from app.services.user_service import update_user_service

from app.schemas.Restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.services.restaurant_service import (
    create_restaurant_service,
    update_restaurant_service,
    #activate_restaurant_service,
    #deactivate_restaurant_service,
    delete_restaurant_service,
    get_restaurant_by_name_service,
    get_restaurant_by_cuisine_service,
    sort_restaurants_by_name_service
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

"""This is where I will keep the endpoints"""

#Create restaurant
@router.post("/", response_model = RestaurantResponse, status_code = 201)
def create_restaurant(payload: RestaurantCreate, token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    require_role_service(current_user, UserRole.STAFF)

    return create_restaurant_service(payload, current_user_id)

#Update Restaurant
@router.put("/update/", response_model = RestaurantResponse)
def update_restaurant(payload: RestaurantUpdate, token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    return update_restaurant_service(payload, current_user_id)

#Delete restaurant
@router.delete("/delete")
def delete_restaurant(token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    delete_restaurant_service(current_user_id)
    return {"message": "Restaurant has been deleted."}


#Get restaurant by name
@router.get("/search/name/{search_name}", response_model = List[RestaurantResponse])
def get_restaurant_by_name(search_name: str):
    return get_restaurant_by_name_service(search_name)


#Get restaurant by cuisine
@router.get("/search/cuisine/{search_cuisine}", response_model = List[RestaurantResponse])
def get_restaurant_by_cuisine(search_cuisine: str):
    return get_restaurant_by_cuisine_service(search_cuisine)



#Sort restaurants by name
@router.get("/sort/name", response_model = List[RestaurantResponse])
def sort_restaurants_by_name():
    return sort_restaurants_by_name_service()


"""NOT UPDATED YET



#Activate restaurant
@router.put("/activate/{restaurant_id}", response_model = RestaurantResponse)
def activate_restaurant(restaurant_id: int):
    return activate_restaurant_service(restaurant_id)

#Deactivate restaurant
@router.put("/deactivate/{restaurant_id}", response_model = RestaurantResponse)
def deactivate_restaurant(restaurant_id: int):
    return deactivate_restaurant_service(restaurant_id)





    """