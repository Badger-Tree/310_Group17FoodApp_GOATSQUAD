from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.routers.restaurants import router
import pytest

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_restaurant_create():
    return{
        "restaurant_name": "Pasta Palace",
        "cuisine": "Italian",
        "address": "123 Test St",
        "open_hour": "11:00",
        "closed_hour": "22:00"
    }

@pytest.fixture
def mock_created_restaurant():
    return {
        "restaurant_id": 1,
        "owner_id": "2",
        "restaurant_name": "Pasta Palace",
        "cuisine": "Italian",
        "address": "123 Test St",
        "open_hour": "11:00:00", #FastAPI makes the date time in this format even though a user enters it as 11:00
        "closed_hour": "22:00:00",
        "restaurant_status": "active"
    }

@pytest.fixture
def mock_user_session():
    return {
        "id" : "2",
        "email" : "test@gmail.com",
        "first_name" : "Test",
        "last_name" : "User",
        "role" : "STAFF",
        "created_date" : "2024-01-01T00:00:00Z"
    }

#this is a sample of what the user send's in to update a restaurant.
@pytest.fixture
def mock_restaurant_update():
    return {
        "restaurant_name": "Luigi's Pizzeria", #name was changed
        "cuisine": "Italian",
        "address": "123 Test St",
        "open_hour": "11:00",
        "closed_hour": "22:00"
    }

@pytest.fixture
def mock_updated_restaurant():
    return {
        "restaurant_id": 1,
        "owner_id": "2",
        "restaurant_name": "Luigi's Pizzeria", #name was changed
        "cuisine": "Italian",
        "address": "123 Test St",
        "open_hour": "11:00:00", #FastAPI makes the date time in this format even though a user enters it as 11:00
        "closed_hour": "22:00:00",
        "restaurant_status": "active"
    }

#Test for restaurant create to see if it is able to create a restaurant
def test_create_restaurant_success(mock_restaurant_create, mock_user_session, mock_created_restaurant):

    #Helper class to turn dictionary data into an object, to try to access the attributes with dot notation since it's was accessed that way in the router
    class MockUserResponse:
        def __init__(self, **kwargs): #kwargs will collect the name value pairs
            self.__dict__.update(kwargs)  #save the name value pairs as attributes of the object

    current_user = MockUserResponse(**mock_user_session) 

    with patch("app.routers.restaurants.get_user_from_session", return_value=current_user):
        with patch("app.routers.restaurants.require_role_service", return_value=None):
            with patch("app.routers.restaurants.create_restaurant_service", return_value=mock_created_restaurant):
                response = client.post(
                    "/restaurants/",
                    json=mock_restaurant_create,
                    headers={"token" : "valid_token"}
                    )
    
    assert response.status_code == 201
    assert response.json() == mock_created_restaurant


#Test to see if restaurant create fails and raises an exception when the user is not authorized to create a restaurant
def test_create_restaurant_failure(mock_restaurant_create, mock_user_session, mock_created_restaurant):

    #Helper class to turn dictionary data into an object, to try to access the attributes with dot notation since it's was accessed that way in the router
    class MockUserResponse:
        def __init__(self, **kwargs): #kwargs will collect the name value pairs
            self.__dict__.update(kwargs)  #save the name value pairs as attributes of the object

    current_user = MockUserResponse(**mock_user_session) 

    with patch("app.routers.restaurants.get_user_from_session", side_effect=HTTPException(status_code=401, detail="Unauthorized")):
        with patch("app.routers.restaurants.require_role_service", return_value=None):
            with patch("app.routers.restaurants.create_restaurant_service", return_value=mock_created_restaurant):
                response = client.post(
                    "/restaurants/",
                    json=mock_restaurant_create,
                    headers={"token" : "valid_token"}
                    )
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


#Test to see if update restaurant will pass when a user with the correct id tries to update a restaurant
def test_update_restaurant_success(mock_user_session, mock_restaurant_update, mock_updated_restaurant):

    #Helper class to turn dictionary data into an object, to try to access the attributes with dot notation since it's was accessed that way in the router
    class MockUserResponse:
        def __init__(self, **kwargs): #kwargs will collect the name value pairs
            self.__dict__.update(kwargs)  #save the name value pairs as attributes of the object

    current_user = MockUserResponse(**mock_user_session) 

    with patch("app.routers.restaurants.get_user_from_session", return_value=current_user):
        with patch("app.routers.restaurants.update_restaurant_service", return_value=mock_updated_restaurant):
            response = client.put(
                "/restaurants/update/",
                json={
                    "restaurant_id": 1,
                    "owner_id": "2",
                    "restaurant_name": "Luigi's Pizzeria", #name was changed
                    "cuisine": "Italian",
                    "address": "123 Test St",
                    "open_hour": "11:00:00", #FastAPI makes the date time in this format even though a user enters it as 11:00
                    "closed_hour": "22:00:00",
                    "restaurant_status": "active"
                },
                headers={"token" : "valid_token"}
                )
    
    assert response.status_code == 200
    
    assert response.json() == mock_updated_restaurant
    

