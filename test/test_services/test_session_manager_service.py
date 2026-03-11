from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.schemas.Role import UserRole
from app.schemas.Token import Token, TokenResponse
from app.schemas.User import UserResponse
from app.services.session_manager_service import create_session_service, expire_session_service, get_user_from_session, validate_token_service
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

def test_create_session_service_success(mocker):
    """tests that create_session_service will create Token if given a use email"""
    mock_user =mocker.Mock()
    mock_user.id = "33"
    mock_user.role = UserRole.CUSTOMER
    
    mock_sessions = [
        {"token": "abc123", "user_id": "1"},
        {"token": "def456", "user_id": "2"}
        ]

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mocker.patch("app.services.session_manager_service.save_sessions", return_value = [])
    mocker.patch("app.services.session_manager_service.get_user_by_email_service", return_value = mock_user)

    result = create_session_service("pippin@example.com")
    assert result.user_id == "33"
    assert result.role == UserRole.CUSTOMER
    assert result.expires > result.created

def test_expire_session_service(mocker):
    """tests that expire_session_service will remove a session record given a token (str)"""
    mock_token = "abc123"
        
    mock_sessions = [
        {"token": "abc123", "user_id": "1"},
        {"token": "def456", "user_id": "2"}
        ]
    
    mock_load_sessions = mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mock_save_sessions = mocker.patch("app.services.session_manager_service.save_sessions")
    
    expire_session_service(mock_token)
    mock_save_sessions.assert_called_once_with([{"token": "def456", "user_id": "2"}])

    
def test_validate_token_service_success(mocker):
    """tests that validate_token_service will return a dictionary with session data if given a Token"""
    mock_token = mocker.Mock()
    mock_token.token="abc123"
    mock_token.user_id = "1"
    mock_token.role= UserRole.CUSTOMER
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    now = datetime.now(timezone.utc).isoformat()
    mock_token.created = now
    mock_token.expires = future
    
    mock_sessions = [
        {"token": "abc123","user_id":"1", "role" : "CUSTOMER", "created" : now,"expires":future}]

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    
    result = validate_token_service(mock_token)
    assert result["token"] == "abc123"
    assert result["user_id"] == "1"  
    assert result["role"] == UserRole.CUSTOMER
    assert result["created"] == now
    assert result["expires"] == future
    
def test_validate_token_service_session_not_found(mocker):
    """tests that validate_token_service will raise an error if a session id not found"""
    mock_token = mocker.Mock()
    mock_token.token="abc"
    mock_token.user_id = "1"
    mock_token.role= UserRole.CUSTOMER
    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    now = datetime.now(timezone.utc).isoformat()
    mock_token.created = now
    mock_token.expires = future
    

    mock_sessions = [
        {"token": "abc123","user_id":"1", "role" : "CUSTOMER", "created" : now,"expires":future}]

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    with pytest.raises(HTTPException) as testException: validate_token_service(mock_token)
    assert testException.value.status_code ==404
    
def test_validate_token_service_session_expired(mocker):
    """tests that validate_token_service will raise an error if a session is expired"""
    mock_token = mocker.Mock()
    mock_token.token="abc123"
    mock_token.user_id = "1"
    mock_token.role= UserRole.CUSTOMER
    past = (datetime.now(timezone.utc) + timedelta(hours=-1)).isoformat()
    now = datetime.now(timezone.utc).isoformat()
    mock_token.created = now
    mock_token.expires = past
    

    mock_sessions = [
        {"token": "abc123","user_id":"1", "role" : "CUSTOMER", "created" : now,"expires":past}]

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    with pytest.raises(HTTPException) as testException: validate_token_service(mock_token)
    assert testException.value.status_code ==401
    
def test_get_user_from_session(mocker):
    """checks that get_user_from_session will return a UserResponse if given a valid session token"""

    future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    now = datetime.now(timezone.utc).isoformat()
    mock_session = {"token": "asdf","user_id":"1", "role" : "CUSTOMER", "created" : now,"expires":future}   
    
    mocker.patch("app.services.session_manager_service.validate_token_service", return_value = mock_session)    

    mock_user = UserResponse(id= "1",
                    email= "pippin@example.com",
                    first_name= "peregrin",
                    last_name= "took",
                    password= "password",
                    role= "CUSTOMER",
                    created_date= datetime.fromisoformat("2026-02-20T12:34:56")
                    )
    
    mocker.patch("app.services.user_service.get_user_by_id_service", return_value = mock_user)
    result = get_user_from_session(Token(token = "asdf"))
        
    assert result.id == mock_user.id
    assert result.role == mock_user.role
    assert result.created_date == mock_user.created_date