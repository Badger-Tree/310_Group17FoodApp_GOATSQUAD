from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from unittest.mock import patch
from app.routers.authentication import router
from app.schemas.Role import UserRole


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

def test_login_success(mocker):
    """tests that login will return a TokenResponse and a 200 message if a user provides valid credentials"""
    mock_LoginRequest = {"email" : "pippin@example.com", "password" : "password"}
    class MockToken:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    mock_token = {"token" : "123", "user_id" : "1", "role" : UserRole.CUSTOMER, "created": "2026-02-20T12:34:56", "expires" : "2026-03-20T12:34:56"}
    
    with patch("app.services.authentication_service.load_users", mock_load_users):
        with patch("app.services.authentication_service.create_session_service", return_value = mock_token):
            response = client.post("/auth/login", json=mock_LoginRequest)
            assert response.status_code == 200
                            
def test_login_invalid_credentials(mocker):
    """tests that login will return a 401 response if user provides invalid login credentials"""
    mock_LoginRequest = {"email" : "wrong@example.com", "password" : "password"}
    
    with patch("app.services.authentication_service.load_users", mock_load_users):
            response = client.post("/auth/login", json=mock_LoginRequest)
            assert response.status_code == 401

def test_login_invalid_email_invalid_format(mocker):
    """tests that login will return a 422 response if user provides email in incorrect format"""
    mock_LoginRequest = {"email" : "wrongexample.com", "password" : "password"}
    
    with patch("app.services.authentication_service.load_users", mock_load_users):
            response = client.post("/auth/login", json=mock_LoginRequest)
            assert response.status_code == 422

def test_logout_success(mocker):
    """tests that logout returns a 200 code after a user successfully logs out"""
    mock_sessions = [{"token": "abc123"}]
    with patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions):
        response = client.post("/auth/logout", headers={"token":"abc123"})
        assert response.status_code == 200
    
def test_logout_session_not_found(mocker):
    """tests that logout returns a 401 unauthorized code if the session passed cannot be located"""
    mock_sessions = [{"token": "abc123"}]
    with patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions):
        response = client.post("/auth/logout", headers={"token":"555"})
        assert response.status_code == 401