import pytest
from app.services.restaurant_service import create_restaurant_service
from app.schemas.Restaurant import RestaurantCreate
import app.services.restaurant_service as restaurant_service

def test_create_restaurant(monkeypatch):

    test_restaurants = []

    #mock loading the restaurants
    def test_load_restaurants():
        return test_restaurants
    
    #mock saving restaurants
    def test_save_restaurants(data):
        test_restaurants[:] = data
    
    #this lets us temporarily modify the original function with our test ones
    monkeypatch.setattr(restaurant_service, "load_restaurants", test_load_restaurants)
    monkeypatch.setattr(restaurant_service, "save_restaurants", test_save_restaurants)

    #payload that matches schema
    payload = RestaurantCreate(
        restaurant_name="Testaurant",
        cuisine="Test Cuisine",
        address="123 Test St",
        open_hour="09:00",
        closed_hour="21:00"
    )


    result = restaurant_service.create_restaurant_service(payload)
    
    #Assertions
    assert result.restaurant_name == "Testaurant"
    assert result.cuisine == "Test Cuisine"
    assert result.address == "123 Test St"
    assert len(test_restaurants) == 1
