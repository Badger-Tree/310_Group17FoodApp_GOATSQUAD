from fastapi import HTTPException
from unittest import result
from datetime import time
import pytest
from app.services.restaurant_service import create_restaurant_service
from app.schemas.Restaurant import RestaurantCreate
import app.services.restaurant_service as restaurant_service


#Test crteating a restaurant
def test_create_restaurant(monkeypatch):

    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    test_users = [
        {
            "id" : "5",
            "email" : "test@gmail.com",
            "first_name" : "Test",
            "last_name" : "User",
            "password" : "password123",
            "role" : "STAFF",
            "created_date" : "2026-02-20T12:34:56"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #mock loading the users
    def test_load_users():
        return test_users
    
    #mock saving users
    def test_save_users(data):
        test_users[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)
    monkeypatch.setattr(restaurant_service, "load_users", test_load_users)
    monkeypatch.setattr(restaurant_service, "save_users", test_save_users)

    #payload that matches schema
    payload = RestaurantCreate(
        restaurant_name="Testaurant",
        cuisine="Test Cuisine",
        address="123 Test St",
        open_hour=time(9, 0),
        closed_hour=time(21, 0)
    )


    result = restaurant_service.create_restaurant_service(payload, test_users[0]["id"])
    
    #Assertions
    assert result.restaurant_name == "Testaurant"
    assert result.cuisine == "Test Cuisine"
    assert result.address == "123 Test St"
    assert result.open_hour == time(9, 0)
    assert result.closed_hour == time(21, 0)
    assert result.restaurant_status == "active"
    assert len(test_restaurants) == 2
    assert test_users[0]["role"] == "OWNER"

#test updating a restaurant
from app.schemas.Restaurant import RestaurantUpdate

def test_update_restaurant(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "2",
            "owner_id": "5",
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese",
            "address": "456 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)


    payload = RestaurantUpdate(
        restaurant_name="Updated Name",
        cuisine="Updated Cuisine",
        address="456 Updated St",
        open_hour=time(10, 0),
        closed_hour=time(22, 0),
        restaurant_status="inactive"
    )

    result = restaurant_service.update_restaurant_service(payload, current_user_id="5")

    #Assertions
    assert result.restaurant_name == "Updated Name"
    assert result.cuisine == "Updated Cuisine"
    assert result.address == "456 Updated St"
    assert result.open_hour == time(10, 0)
    assert result.closed_hour == time(22, 0)
    assert result.restaurant_status == "inactive"

    assert test_restaurants[1]["restaurant_name"] == "Updated Name"
    assert test_restaurants[1]["cuisine"] == "Updated Cuisine"
    assert test_restaurants[1]["address"] == "456 Updated St"
    assert test_restaurants[1]["open_hour"] == "10:00"
    assert test_restaurants[1]["closed_hour"] == "22:00"
    assert test_restaurants[1]["restaurant_status"] == "inactive"

#test deleting a restaurant success
def test_delete_restaurant(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)

    restaurant_service.delete_restaurant_service("1")

    #Assertions
    assert len(test_restaurants) == 0

#test deleting a restaurant failure
def test_delete_restaurant_failure(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)


    #I am expecting the code inside this pytest wrapper to raise this exception and save the info to exc_info.
    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.delete_restaurant_service("2")

    #Assertions
    assert len(test_restaurants) == 1
    assert test_restaurants[0]["restaurant_id"] == "1"
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant not found or you do not have permission to delete it"

#test getting a restaurant by name success
def test_get_restaurant_by_name(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.get_restaurant_by_name_service("mario")

    #Assertions
    assert result is not None
    assert len(result) == 1
    assert result[0].restaurant_name == "Mario's Pizza"

#test getting a restaurant by name failure (no match)
def test_get_restaurant_by_name_failure(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.get_restaurant_by_name_service("pasta")

    #Assertions
    assert result == []
    assert len(result) == 0

#test getting a restaurant by cuisine: Success
def test_get_restaurant_by_cuisine_success(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "2",
            "owner_id": "2",
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese",
            "address": "456 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "3",
            "owner_id": "3",
            "restaurant_name": "Taco Time",
            "cuisine": "Mexican",
            "address": "457 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.get_restaurant_by_cuisine_service("japanese")

    #Assertions
    assert result is not None
    assert len(result) == 1
    assert result[0].restaurant_name == "Sakura Sushi"
    assert result[0].cuisine == "Japanese"

#test getting a restaurant by cuisine: Failure, no restaurant matches the cuisine
def test_get_restaurant_by_cuisine_failure(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "2",
            "owner_id": "2",
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese",
            "address": "456 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "3",
            "owner_id": "3",
            "restaurant_name": "Taco Time",
            "cuisine": "Mexican",
            "address": "457 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.get_restaurant_by_cuisine_service("indian")

    #Assertions
    assert result == []
    assert len(result) == 0

#test sorting restaurant by name: SUCCESS
def test_sort_restaurants_by_name_success(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "2",
            "owner_id": "2",
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese",
            "address": "456 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        },
        {
            "restaurant_id": "3",
            "owner_id": "3",
            "restaurant_name": "Pasta Palace",
            "cuisine": "Italian",
            "address": "457 Elm St",
            "open_hour": "10:00",
            "closed_hour": "22:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.sort_restaurants_by_name_service()

    #Assertions
    assert len(result) == 3
    assert result[0].restaurant_name == "Mario's Pizza"
    assert result[1].restaurant_name == "Pasta Palace"
    assert result[2].restaurant_name == "Sakura Sushi"

#test sorting restaurants by name: FAILURE, no restaurants to sort
def test_sort_restaurants_by_name_failure(monkeypatch):
    test_restaurants=[]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)

    result = restaurant_service.sort_restaurants_by_name_service()

    #Assertions
    assert len(result) == 0
    assert result == []



""" NOT YET UPDATED 






#test activating a restaurant
def test_activate_restaurant(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "inactive"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)

    result = restaurant_service.activate_restaurant_service(1)

    #Assertions
    assert result.restaurant_status == "active"
    assert test_restaurants[0]["restaurant_status"] == "active"


#test deactivating a restaurant
def test_deactivate_restaurant(monkeypatch):
    test_restaurants = [
        {
            "restaurant_id": "1",
            "owner_id": "1",
            "restaurant_name": "Mario's Pizza",
            "cuisine": "Italian",
            "address": "123 Main St",
            "open_hour": "09:00",
            "closed_hour": "21:00",
            "restaurant_status": "active"
        }
    ]

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)

    result = restaurant_service.deactivate_restaurant_service(1)

    #Assertions
    assert result.restaurant_status == "inactive"
    assert test_restaurants[0]["restaurant_status"] == "inactive"



    """