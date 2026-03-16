from datetime import datetime
from fastapi import HTTPException
from app.schemas.Login import LoginRequest
from app.schemas.Role import UserRole
from app.schemas.Token import Token, TokenResponse
from app.repositories.users_repo_csv import load_all as load_users
from app.services.authentication_service import login_service, logout_service, validate_credentials
import pytest

mock_users = {
        "id": "1",
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }

mock_token = TokenResponse(token="abc", 
                            user_id = "1", 
                            role= "CUSTOMER",
                            created = "2026-02-20T12:34:56",
                            expires = "2026-03-20T12:34:56")

def test_login_service_success(mocker):
    """Tests if login_service will successfully return a token if provided email and password matching to user in system"""
    input_data = LoginRequest(email = "pippin@example.com", password = "password")

    mocker.patch("app.services.authentication_service.validate_credentials", return_value = True)
    mocker.patch("app.services.authentication_service.create_session_service", return_value=mock_token)
    
    result = login_service(input_data)
    assert result ==mock_token
    assert mock_token.token == "abc"
    assert mock_token.user_id == "1"
    assert mock_token.role == UserRole.CUSTOMER
    assert mock_token.created == datetime.fromisoformat("2026-02-20T12:34:56")
    assert mock_token.expires == datetime.fromisoformat("2026-03-20T12:34:56")

def test_login_service_invalid_credentials(mocker):
    """tests that login_service will raise an exception if the email and password do not match a registered user (validate_credentials erturns false)"""
    input_data = LoginRequest(email = "email@email.com", password = "password")

    mocker.patch("app.services.authentication_service.validate_credentials", return_value = False)
    mocker.patch("app.services.authentication_service.create_session_service", return_value=mock_token)
    
    with pytest.raises(HTTPException) as testException: login_service(input_data)
    assert testException.value.status_code ==401
    
def test_logout_service_success(mocker):
    """tests that logout_service will successfully end a session if given a valid token"""
    
    mock_sessions = [
    {"token": "abc123", "user_id": "1"},
    {"token": "def456", "user_id": "2"}
    ]
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions) 
    mocker.patch("app.services.session_manager_service.save_sessions", return_value = [])
    token = Token(token="abc123")
    
    result = logout_service(token)
    assert result == {"detail": "logout successful"}
    
def test_logout_service_success(mocker):
    """tests that logout_service will raise an excpetion if given invalid session"""
    mock_sessions = [
    {"token": "abc123", "user_id": "1"},
    {"token": "def456", "user_id": "2"}
    ]
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions) 
    mocker.patch("app.services.session_manager_service.save_sessions", return_value = [])
    token = Token(token="55555")
    with pytest.raises(HTTPException) as testException: logout_service(token)
    assert testException.value.status_code ==401
    
def test_validate_credentials_success(mocker):
    """checks that validate_credentials() will return True if given a valid email and password that match a registered user"""
    input_email = "pippin@example.com" 
    input_password = "password"
  
    mock_users = [{
        "id": "1",
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    mocker.patch("app.services.authentication_service.load_users", return_value = mock_users)
    result = validate_credentials(input_email, input_password)
    assert result == True

def test_validate_credentials_wrong_password(mocker):
    """checks that validate_credentials() will return False if given a non-matching password"""
    input_email = "pippin@example.com" 
    input_password = "wrong_password"
  
    mock_users = [{
        "id": "1",
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    mocker.patch("app.services.authentication_service.load_users", return_value = mock_users)
    result = validate_credentials(input_email, input_password)
    assert result == False
    
def test_validate_credentials_user_not_found(mocker):
    """checks that validate_credentials() will return False if given a non-matching email"""
    input_email = "wrong_pippin@example.com" 
    input_password = "password"
  
    mock_users = [{
        "id": "1",
        "email": "pippin@example.com",
        "first_name": "peregrin",
        "last_name": "took",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    mocker.patch("app.services.authentication_service.load_users", return_value = mock_users)
    result = validate_credentials(input_email, input_password)
    assert result == False