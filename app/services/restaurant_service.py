from typing import List
from fastapi import HTTPException
from dateutil import parser


"""This is pulling the csv file and the functions from the restaurant file in repositories. """
from app.repositories.restaurants_repo_csv import load_all as load_restaurants, save_all as save_restaurants
"""This is getting the restaurant schema and the the other classes in that file"""
from app.schemas.Restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse

"""Service for creating a restaurant"""
def create_restaurant_service(payload: RestaurantCreate, owner_id: str) -> RestaurantResponse:
    restaurants = load_restaurants()

    #Auto-increment the restaurant id
    if restaurants:
        new_id = max(int(r["restaurant_id"]) for r in restaurants) + 1
    else:
        new_id = 1
    
    #Basic validation - no blank restaurant names
    if not payload.restaurant_name.strip():
        raise HTTPException(status_code=400, detail="Restaurant name cannot be blank")
    
    open_time = parser.parse(payload.open_hour).time()
    closed_time = parser.parse(payload.closed_hour).time()
    new_restaurant = {
        "restaurant_id": str(new_id),
        "owner_id": str(owner_id),
        "restaurant_name": payload.restaurant_name.strip(),
        "cuisine": payload.cuisine.strip(),
        "address": payload.address.strip(),
        "open_hour": open_time.strftime("%H:%M"),
        "closed_hour": closed_time.strftime("%H:%M"),
        "restaurant_status": "active"
    }

    restaurants.append(new_restaurant)
    save_restaurants(restaurants)

    #return the restaurant response
    return RestaurantResponse(
        restaurant_id = new_id,
        owner_id = owner_id,
        restaurant_name = new_restaurant["restaurant_name"],
        cuisine = new_restaurant["cuisine"],
        address = new_restaurant["address"],
        open_hour = new_restaurant["open_hour"],
        closed_hour = new_restaurant["closed_hour"],
        restaurant_status = new_restaurant["restaurant_status"]
    )

"""Service for updating a restaurant."""
def update_restaurant_service(restaurant_id: int, payload: RestaurantUpdate) -> RestaurantResponse:
    restaurants = load_restaurants()

    updated = None
    for i, r in enumerate(restaurants):
        if int(r["restaurant_id"]) == restaurant_id:
            if payload.restaurant_name is not None:
                r["restaurant_name"] = payload.restaurant_name.strip()
            if payload.cuisine is not None:
                r["cuisine"] = payload.cuisine.strip()
            if payload.address is not None:
                r["address"] = payload.address.strip()
            if payload.open_hour is not None:
                r["open_hour"] = payload.open_hour.strftime("%H:%M").strip()
            if payload.closed_hour is not None:
                r["closed_hour"] = payload.closed_hour.strftime("%H:%M").strip()
            if payload.restaurant_status is not None:
                r["restaurant_status"] = payload.restaurant_status.strip()
            
            restaurants[i] = r
            updated = r
            break

    if updated is None:
        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} not found")
        
    save_restaurants(restaurants)

    return RestaurantResponse(
        restaurant_id = int(updated["restaurant_id"]),
        owner_id = int(updated["owner_id"]),
        restaurant_name = updated["restaurant_name"],
        cuisine = updated["cuisine"],
        address = updated["address"],
        open_hour = updated["open_hour"],
        closed_hour = updated["closed_hour"],
        restaurant_status = updated["restaurant_status"]
    )
    
"""Service for activating a restaurant."""
def activate_restaurant_service(restaurant_id: int) -> RestaurantResponse:
    restaurants = load_restaurants()

    updated = None

    #To activate the restautant, change the status to active
    for i, r in enumerate(restaurants):
        if int(r["restaurant_id"]) == restaurant_id:
            r["restaurant_status"] = "active"
            restaurants[i] = r
            updated = r
            break

    if updated is None:
        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} not found")
        
    save_restaurants(restaurants)

    return RestaurantResponse(
        restaurant_id = int(updated["restaurant_id"]),
        owner_id = int(updated["owner_id"]),
        restaurant_name = updated["restaurant_name"],
        cuisine = updated["cuisine"],
        address = updated["address"],
        open_hour = updated["open_hour"],
        closed_hour = updated["closed_hour"],
        restaurant_status = updated["restaurant_status"]
    )
    
"""Service for deactivating a restaurant"""
def deactivate_restaurant_service(restaurant_id: int) -> RestaurantResponse:
    restaurants = load_restaurants()

    #To deactivate a restaurant, change the status to inactive
    updated = None
    for i, r in enumerate(restaurants):
        if int(r["restaurant_id"]) == restaurant_id:
            r["restaurant_status"] = "inactive"
            restaurants[i] = r
            updated = r
            break

    if updated is None:
        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} not found")
        
    save_restaurants(restaurants)

    return RestaurantResponse(
        restaurant_id = int(updated["restaurant_id"]),
        owner_id = int(updated["owner_id"]),
        restaurant_name = updated["restaurant_name"],
        cuisine = updated["cuisine"],
        address = updated["address"],
        open_hour = updated["open_hour"],
        closed_hour = updated["closed_hour"],
        restaurant_status = updated["restaurant_status"]
    )
    
"""Service for deleting a restaurant."""
def delete_restaurant_service(restaurant_id: int) -> None:
    restaurants = load_restaurants()

    found = False
    for i, r in enumerate(restaurants):
        if int(r["restaurant_id"]) == restaurant_id:
            found = True
            restaurants.pop(i)
            break

    if not found:
        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} not found")
        
    save_restaurants(restaurants)

"""Service for getting a restaurant by name"""
def get_restaurant_by_name_service(search_name: str) -> List[RestaurantResponse]:
    restaurants = load_restaurants()
    results = []
    for r in restaurants:
        if search_name.lower().strip() in r["restaurant_name"].lower().strip():
            results.append(
                RestaurantResponse(
                    restaurant_id = int(r["restaurant_id"]),
                    owner_id = int(r["owner_id"]),
                    restaurant_name = r["restaurant_name"],
                    cuisine = r["cuisine"],
                    address = r["address"],
                    open_hour = r["open_hour"],
                    closed_hour = r["closed_hour"],
                    restaurant_status = r["restaurant_status"]
                )
            )
    return results
    
"""Service for getting a restaurant by cuisine"""
def get_restaurant_by_cuisine_service(search_cuisine: str) -> List[RestaurantResponse]:
    restaurants = load_restaurants()
    results = []
    for r in restaurants:
        if search_cuisine.lower().strip() in r["cuisine"].lower().strip():
            results.append(
                RestaurantResponse(
                    restaurant_id = int(r["restaurant_id"]),
                    owner_id = int(r["owner_id"]),
                    restaurant_name = r["restaurant_name"],
                    cuisine = r["cuisine"],
                    address = r["address"],
                    open_hour = r["open_hour"],
                    closed_hour = r["closed_hour"],
                    restaurant_status = r["restaurant_status"]
                )
            )
    return results
    
"""Service for sorting the restaurants by their name"""
def sort_restaurants_by_name_service() -> List[RestaurantResponse]:
    restaurants = load_restaurants()
            
    #sort alphabetically by name
    sorted_restaurants = sorted(restaurants, key=lambda r: r["restaurant_name"].lower())

    results = []
    for r in sorted_restaurants:
        results.append(
            RestaurantResponse(
                restaurant_id = int(r["restaurant_id"]),
                owner_id = int(r["owner_id"]),
                restaurant_name = r["restaurant_name"],
                cuisine = r["cuisine"],
                address = r["address"],
                open_hour = r["open_hour"],
                closed_hour = r["closed_hour"],
                restaurant_status = r["restaurant_status"]
            )
        )
    return results