from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from unittest.mock import patch
from app.routers.user import get_user_by_id, router
from app.services.user_service import get_user_by_id_service 

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def mock_load_users():
        return [{
        "id": "1",
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]

def mock_save_users(*args, **kwargs):
    return None
        
mock_user_response = {
        "email": "pippin@example.com",
        "id": "1",
        "first_name": "peregrin",
        "last_name": "took",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }
mock_user_update_response = {
        "email": "new@example.com",
        "id": "1",
        "first_name": "peregrin",
        "last_name": "took",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }
        
mock_customer_create = {
        "email": "merry@example.com",
        "first_name": "meriadoc",
        "last_name": "brandybuck",
        "password" : "password"
        }
        
def test_get_user_by_id_success(mocker):
    """tests that the get_user_by_id will return a UserResponse if a user is found"""
    with patch("app.services.user_service.load_users", mock_load_users):
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json() == mock_user_response

        
def test_get_user_by_id_not_found(mocker):
    """tests that the get_user_by_id will throw a 404 exception if a user is not found"""
    with patch("app.services.user_service.load_users", mock_load_users):
        response = client.get("/users/2")
        assert response.status_code == 404

def test_get_user_by_email_success(mocker):
    """tests that the get_user_by_email will return a UserResponse if a user is found"""
    with patch("app.services.user_service.load_users", mock_load_users):
        response = client.get("/users/by-email/pippin@example.com")
        assert response.status_code == 200
        assert response.json() == mock_user_response

def test_get_user_by_email_not_found(mocker):
    """tests that the get_user_by_id will throw a 404 exception if a matching user is not found"""
    with patch("app.services.user_service.load_users", mock_load_users):
        response = client.get("/users/by-email/merry@example.com")
        assert response.status_code == 404

def test_get_user_by_email_incorrect_format(mocker):
    """tests that the get_user_by_id will throw a 404 exception if an incorrectly formatted email is submitted"""
    with patch("app.services.user_service.load_users", mock_load_users):
        response = client.get("/users/by-email/pippinexample.com")
        assert response.status_code == 404
#customer
def test_register_customer_success(mocker):
    """tests that register_customer will return a 201 response if a customer is successfully created"""
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-customer", json = mock_customer_create)
            assert response.status_code == 201

def test_register_customer_duplicate_user(mocker):
    """tests that register_customer will throw a 409 response if a provided email is a duplicate"""
    mock_duplicate_customer_create = {
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password" : "password"
        }
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-customer", json = mock_duplicate_customer_create)
            assert response.status_code == 409

def test_register_customer_incomplete_input(mocker):
    """tests that register_customer will return a 422 response if incomplete json data is provided"""
    mock_missing_customer_create = {
        "first_name": "peregrin",
        "last_name": "took",
        "password" : "password"
        }
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-customer", json = mock_missing_customer_create)
            assert response.status_code == 422
#staff

def test_register_staff_success(mocker):
    """tests that register_staff will return a 201 response if a user is successfully created"""
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-staff", json = mock_customer_create)
            assert response.status_code == 201
            
def test_register_staff_duplicate_user(mocker):
    """tests that register_staff will throw a 409 response if a provided email is a duplicate"""
    mock_duplicate_staff_create = {
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password" : "password"
        }
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-staff", json = mock_duplicate_staff_create)
            assert response.status_code == 409

def test_register_staff_incomplete_input(mocker):
    """tests that register_staff will throw a 422 response if incomplete json data is provided"""
    mock_missing_staff_create = {
        "first_name": "peregrin",
        "last_name": "took",
        "password" : "password"
        }
    with patch("app.services.user_service.load_users", mock_load_users):
        with patch("app.services.user_service.save_all_users", mock_save_users):
            response = client.post("/users/new-staff", json = mock_missing_staff_create)
            assert response.status_code == 422
            
def test_update_user_success(mocker):
    """tests that update_user will successfully update a user given valid input"""
    class MockUserResponse:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    mock_user_update = {
        "email": "new@example.com"
        }  
    with patch("app.services.user_service.load_users", side_effect = mock_load_users):
        with patch("app.services.user_service.save_all_users", side_effect = mock_save_users):
            with patch("app.routers.user.get_user_from_session", return_value = MockUserResponse(**mock_user_response)):
                response = client.put("/users/update-user/", json=mock_user_update, headers={"token":"123"})
                assert response.status_code == 200
                
def test_update_user_success_multiple_fields(mocker):
    """tests that update_user will successfully update a user given valid input across multiple fields"""
    class MockUserUpdate:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    mock_user_update = {
        "email": "new@example.com",
        "first_name" : "Gandalf",
        "last_name" : "White",
        "password" : "friend"
        }  
    with patch("app.services.user_service.load_users", side_effect = mock_load_users):
        with patch("app.services.user_service.save_all_users", side_effect = mock_save_users):
            with patch("app.routers.user.get_user_from_session", return_value = MockUserUpdate(**mock_user_response)):
                response = client.put("/users/update-user/", json=mock_user_update, headers={"token":"123"})
                assert response.status_code == 200
                                
def test_update_user_no_update_fields_success(mocker):
    """tests that update_user_will process an update request if no input fields are provided"""
    class MockUser:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    mock_user_update = {}  
    with patch("app.services.user_service.load_users", side_effect = mock_load_users):
        with patch("app.services.user_service.save_all_users", side_effect = mock_save_users):
            with patch("app.routers.user.get_user_from_session", return_value = MockUser(**mock_user_response)):
                response = client.put("/users/update-user/", json=mock_user_update, headers={"token":"123"})
                assert response.status_code == 200
                   
def test_update_user_not_authenticated(mocker):
    """tests that update_user will return a 422 response if a non-logged in user tries to use router"""
    mock_user_update = {
        "email": "new@example.com"
        }  
    with patch("app.services.user_service.load_users", side_effect = mock_load_users):
        with patch("app.services.user_service.save_all_users", side_effect = mock_save_users):
            with patch("app.routers.user.get_user_from_session", side_effect=HTTPException(status_code=404, detail="User not found")):
                response = client.put("/users/update-user/", json=mock_user_update, headers={"token":"123"})
                assert response.status_code == 404

def test_update_user_missing_token():
    """Tests that FastAPI will throw an exception if there is no token in the header"""
    mock_user_update = {"email": "new@example.com"}  
    response = client.put("/users/update-user/", json = mock_user_update)
    assert response.status_code == 422
    