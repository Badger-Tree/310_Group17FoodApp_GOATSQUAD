from datetime import datetime
import pytest

from fastapi import HTTPException
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, UserUpdate
from app.services.user_service import get_user_by_id_service, get_user_by_email_service, register_user_service, update_user_service

def test_get_user_by_id_service_success(monkeypatch):
    """tests that get_user_by_id_service() will successfully return a UserResponse given valid input"""
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
    """tests that get_user_by_id_service() will generate an error if a user id cannot be found"""
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
    with pytest.raises(HTTPException, match = "User '77' not found") as testException: get_user_by_id_service("77")
    assert testException.value.status_code ==404
    
    
def test_get_user_by_email_service_found(monkeypatch):
    """tests that get_user_by_email_service() will successfully return a UserResponse given valid input"""
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

def test_get_user_by_email_service_caseinsensitive(monkeypatch):
    """tests that get_user_by_email_service() will successfully return a UserResponse given emails that do not match in case"""
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

def test_get_user_by_email_service_notfound(monkeypatch):
    """tests that get_user_by_email_service() will create an error if it cannot find a user email"""
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
    """Tests that register_user_service() successfully makes a customer record given valid input"""
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
        return []

    saved_users = []
    def mock_save_all_users(users):
        nonlocal saved_users
        saved_users = users.copy()
  
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.user_service.save_all_users", mock_save_all_users)
    monkeypatch.setattr("app.services.user_service.CustomerFactory", MockCustomerFactory)
    payload = CustomerCreate(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="password"
    )
    result = register_user_service(payload, UserRole.CUSTOMER)
    
    assert result.id == "1"
    assert result.email == "test@example.com"
    assert saved_users[0]["password"] == "password"

def test_register_user_service_staff_success(monkeypatch):
    """Tests that register_user_service() successfully makes a staff record given valid input"""
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
    """Tests that register_user_service() creates an error message if there is already an account with the provided email"""
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
    """Tests that update_user_service() successfully updates a customer record given valid input"""
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
    updated_user = update_user_service("1", payload)
    assert updated_user.id == "1"
    assert updated_user.first_name == "UpdatedJane"
    assert updated_user.last_name == "doe"
    assert saved_users[0]["password"] == "UpdatedPassword"
 
def test_update_user_service_usernotfound(monkeypatch):
    """Tests that update_user_service() creates an error message if there is no user found with provided user id"""
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
    with pytest.raises(HTTPException, match = "User 77 not found") as testException: update_user_service("77", payload)
    assert testException.value.status_code ==404
