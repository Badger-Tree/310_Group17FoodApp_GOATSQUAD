from datetime import datetime
import pytest
## I'm using monkeypatch, which is part of pytest, but there are other mock and patching dictionaries (e.g. unittest.mock that I read about)
## Monkeypatching dynamically changes the code during runtime. This is important in unit testing because
## it will redirect inputs/methods during your test to mock data instead of real data. I think that in unit tests we are just testing 
## how the methods input/output data, so we don't want to connect to other parts of the project (e.g. schemas, routers, etc). We will 
## do that in integration testing. But if there are issues in how the router gets info, we dont want that affecting how we unit test a service.
## That's how I understand, hope it is right.
 
from fastapi import HTTPException
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, UserUpdate
from app.services.user_service import list_users, get_user_by_id_service, get_user_by_email_service, register_user_service, update_user_service


#This test is testing list_users() from user_services 
#Test methods need to intake monkeypatch (or whatever patch method)
def test_list_users(monkeypatch):

    def mock_load_users():
    ## mock_load_users() is creating a mock version of load_users() from the real list_users() method. This is the method from 
    ## repositories that loads all data from the csv. For the purposes of the test, we don't want the real production data, we want to give 
    ## it fake data. So this mock method just returns a dictionary with the same fields/format that the real load_users() would.
    ## My example only has one element, but there can be many. I saw people use decorators to parameterize the input to have multiple 
    ## input values, but I didn't do that here.
    
    ## You could also define the mock method/data outside and then re-use it in every test. I was having issues doing that but I 
    ## might try again since my code is really messy/has lots of repeats.
    
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    ## This method is declaring where/how to redirect data. 
    ## syntax: monkeypatch.setattr("real method that you want to redirect away from", mock method)
    
    result = list_users()
    ## call the real method that you're testing and hold in variable. Then test the outcome using assert.
    assert len(result) == 1
    assert result[0].id == "1";
    assert result[0].email == "jane.doe@example.com"
    assert result[0].first_name == "jane"
    assert result[0].last_name == "doe"
    
def test_get_user_by_id_service_success(monkeypatch):
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
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    result = get_user_by_id_service("1")
    assert result.id == "1"
    assert result.first_name == "peregrin"
    assert result.last_name == "took"
    assert result.email == "pippin@example.com"
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")

def test_get_user_by_id_service_notfound(monkeypatch):
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
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    ## In this test I want to test what happens when it fails, which should be an http exception. 
    ## I'm not asserting anything do do with the attributes, since I know nothing will be found. My data only has 
    ## one element with id == "1" and I'm testing id == "77".
    with pytest.raises(HTTPException, match = "User '77' not found") as testException: get_user_by_id_service("77")
    assert testException.value.status_code ==404
    
    
def test_get_user_by_email_service_found(monkeypatch):
    def mock_load_users():
            return [{
            "id": "1",
            "email": "jane.doe@example.com",
            "first_name": "jane",
            "last_name": "doe",
            "password": "password",
            "role": "CUSTOMER",
            "created_date": "2026-02-20T12:34:56"
            }]
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    
    result = get_user_by_email_service("jane.doe@example.com")
    assert result.id == "1"
    assert result.first_name == "jane"
    assert result.last_name == "doe"
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")


def test_get_user_by_email_service_notfound(monkeypatch):
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    
    result = get_user_by_email_service("Jane.Doe@example.com")
    assert result.id == "1"
    assert result.first_name == "jane"
    assert result.last_name == "doe"
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")


def test_get_user_by_email_service_caseinsensitive(monkeypatch):
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    with pytest.raises(HTTPException, match = "User 'john.doe@example.com' not found") as testException: get_user_by_email_service("john.doe@example.com")
    assert testException.value.status_code ==404

def test_register_user_service_customer_success(monkeypatch):
    class MockCustomerFactory:
        ## this is mocking the factory methods. Since it's a unit test I don't want to connect to the actual factory itself, 
        ## so I'm mocking its input/output
        def create_user(self, payload):
            return {"id":"1",
                    "email": payload.email,
                    "first_name": payload.first_name,
                    "last_name": payload.last_name,
                    "password": payload.password,
                    "role": "CUSTOMER",
                    "created_date": "2026-02-20T12:34:56"}
    def mock_load_users():
        return []
        ## load_users returns an empty list in this method since I don't need any existing data
    
    ## Here I'm also mocking saving the save_all_users method, which in the real version is from repositories
    ## I don't want to save any actual data, so I'm sending the input from the real method to mock_save_all_users and then 
    ## copying that data to saved_users. I don't know if this is right.
    saved_users = []
    def mock_save_all_users(users):
        ##non-local lets the function edit the list from outside the loop instead of making a new one.
        nonlocal saved_users
        saved_users = users.copy()
  
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)
    monkeypatch.setattr("app.services.user_service.CustomerFactory", MockCustomerFactory)
    payload = CustomerCreate(
        ## this is a mock of the CustomerCreate payload, which is the input for the real method. 
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="password"
    )
    result = register_user_service(payload, UserRole.CUSTOMER)
    
    ## id and email are part of the UserResponse model, so they can be tested from result.
    assert result.id == "1"
    assert result.email == "test@example.com"
    ## password isn't part of the response model, so it can't be tested in the same way. Instead I'm testing in the list saved
    ## in the mock_save_all_users() method. Again, not sure if this is right.
    assert saved_users[0]["password"] == "password"

def test_register_user_service_staff_success(monkeypatch):
    class MockCustomerFactory:
        def create_user(self, payload):
            return {"id":"1",
                    "email": payload.email,
                    "first_name": payload.first_name,
                    "last_name": payload.last_name,
                    "password": payload.password,
                    "role": "STAFF",
                    "created_date": "2026-02-20T12:34:56"}
    def mock_load_users():
        return []
    saved_users = []
    def mock_save_all_users(users):
        nonlocal saved_users
        saved_users = users.copy()
  
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)
    monkeypatch.setattr("app.services.user_service.CustomerFactory", MockCustomerFactory)
    payload = CustomerCreate(
        email="test@business.com",
        first_name="Test",
        last_name="Staff",
        password="password"
    )
    result = register_user_service(payload, UserRole.CUSTOMER)
    assert result.id == "1"
    assert result.email == "test@business.com"
    assert result.first_name == "Test"
    assert result.last_name == "Staff"
    assert result.role == "STAFF"
    assert saved_users[0]["password"] == "password"

def test_register_user_service_duplicate_email(monkeypatch):
    class MockCustomerFactory:
        def create_user(self, payload):
            return {"id":"1",
                    "email": payload.email,
                    "first_name": payload.first_name,
                    "last_name": payload.last_name,
                    "password": payload.password,
                    "role": "CUSTOMER",
                    "created_date": "2026-02-20T12:34:56"}
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    def mock_save_all_users(users):
        return users
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)
    monkeypatch.setattr("app.services.user_service.CustomerFactory", MockCustomerFactory)
    payload = CustomerCreate(
        email="jane.doe@example.com",
        first_name="Test",
        last_name="User",
        password="password"
    )
    
    with pytest.raises(HTTPException, match = "Account with that email already exists") as testException: register_user_service(payload, UserRole.CUSTOMER)
    assert testException.value.status_code ==409
    
def test_update_user_service_success(monkeypatch):
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    saved_users = []
    def mock_save_all_users(users):
        nonlocal saved_users
        saved_users = users.copy()
        
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)
    
    payload = UserUpdate(first_name = "UpdatedJane", last_name = None, password = "UpdatedPassword")
    updated_user = update_user_service("1", payload, role="CUSTOMER")
    assert updated_user.id == "1"
    assert updated_user.first_name == "UpdatedJane"
    assert updated_user.last_name == "doe"
    assert saved_users[0]["password"] == "UpdatedPassword"
 
def update_user_service_usernotfound(monkeypatch):
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    saved_users = []
    def mock_save_all_users(users):
        nonlocal saved_users
        saved_users = users.copy()
        
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)

    payload = UserUpdate(first_name = "UpdatedJane", last_name = None, password = "UpdatedPassword")
    
    with pytest.raises(HTTPException, match = "User 77 not found") as testException: update_user_service_usernotfound("77", payload, role="CUSTOMER")
    assert testException.value.status_code ==404
