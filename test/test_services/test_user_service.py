from datetime import datetime
import pytest
from fastapi import HTTPException

from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate
from app.services.user_service import list_users, get_user_by_id_service, get_user_by_email_service, register_user_service, update_user_service
## monkeypatching dynamically changes the code during runtime
# id,email,first_name,last_name,password,role,created_date



        



##note, could also 
def test_list_users(monkeypatch):
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
    
    result = list_users()
    assert len(result) == 1
    assert result[0].id == "1";
    assert result[0].email == "jane.doe@example.com"
    
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

def test_register_user_service_customer_success(monkeypatch):
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
    def mock_save_all_users(users):
        return users
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
    assert result.first_name == "Test"
    assert result.last_name == "User"
    assert result.role == "CUSTOMER"

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
    def mock_save_all_users(users):
        return users
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


# test_register_user_service_duplicate_email
# test_register_user_service_invalid_role

# update_user_service_success
# update_user_service_usernotfound
