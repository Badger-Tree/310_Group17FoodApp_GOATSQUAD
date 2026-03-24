from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.schemas.Role import UserRole
from app.schemas.Token import Token, TokenResponse
from app.schemas.User import UserResponse
from app.services.session_manager_service import create_session_service, expire_session_service, get_session_from_token, get_user_from_session, validate_token_service
import pytest

@pytest.fixture
def mock_users():
    return [{
            "id": "1",
            "email": "pippin@example.com",
            "first_name": "peregrin",
            "last_name": "took",
            "password": "password",
            "role": "CUSTOMER",
            "created_date": "2026-02-20T12:34:56"
            }]

@pytest.fixture
def mock_user_response():
    return UserResponse(id= "1",
                    email= "pippin@example.com",
                    first_name= "peregrin",
                    last_name= "took",
                    password= "password",
                    role= "CUSTOMER",
                    created_date= datetime.fromisoformat("2026-02-20T12:34:56")
                    )

@pytest.fixture
def mock_sessions():
    return  [{"token": "abc123","user_id":"1", "role" : "CUSTOMER", "created": "2026-02-20T12:34:56+00:00","expires": "2026-03-20T12:34:56+00:00",},
                {"token": "abc456","user_id":"1", "role" : "CUSTOMER", "created" : "2026-02-20T12:34:56+00:00","expires":"2026-03-20T12:34:56+00:00"},
                {"token": "abc789","user_id":"2", "role" : "STAFF", "created" : "2026-02-20T12:34:56+00:00","expires":"2026-01-20T12:34:56+00:00"}]


def test_create_session_service_success(mocker, mock_sessions, mock_user_response):
    """tests that create_session_service will create Token if given a use email"""

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mocker.patch("app.services.session_manager_service.save_sessions", return_value = [])
    mocker.patch("app.services.session_manager_service.get_user_by_email_service", return_value = mock_user_response)

    result = create_session_service("pippin@example.com")
    assert result.user_id == "1"
    assert result.role == UserRole.CUSTOMER
    assert result.expires > result.created

def test_expire_session_service(mocker,mock_sessions):
    """tests that expire_session_service will remove a session record given a token (str)"""
    mock_token = "abc123"
    
    mock_load_sessions = mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mock_save_sessions = mocker.patch("app.services.session_manager_service.save_sessions")
    
    expire_session_service(mock_token)
    mock_save_sessions.assert_called_once()
    mock_load_sessions.assert_called_once()
    saved_data = mock_save_sessions.call_args[0][0]
    assert len(saved_data) == 2

def test_validate_token_service_success(mocker,mock_sessions):
    """tests that validate_token_service will return a dictionary with session data if given a valid Token that is not expired"""
    mock_token = mocker.Mock()
    mock_token.token="abc123"
    mock_now = datetime.fromisoformat("2026-03-20T12:34:55+00:00")
    
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mocker.patch("app.services.session_manager_service.datetime", wraps = datetime).now.return_value = mock_now
    
    
    
    result = validate_token_service(mock_token)
    assert result["token"] == "abc123"
    assert result["user_id"] == "1"  
    assert result["role"] == UserRole.CUSTOMER
    assert result["created"] == datetime.fromisoformat("2026-02-20T12:34:56+00:00").isoformat()
    assert result["expires"] == datetime.fromisoformat("2026-03-20T12:34:56+00:00").isoformat()

def test_validate_token_service_session_not_found(mocker,mock_sessions):
    """tests that validate_token_service will raise an error if a session id not found"""
    mock_token = mocker.Mock()
    mock_token.token="abc"

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    with pytest.raises(HTTPException) as testException: validate_token_service(mock_token)
    assert testException.value.status_code ==404
    
def test_validate_token_service_session_expired(mocker,mock_sessions):
    """tests that validate_token_service will raise an error if a session is expired"""
    mock_token = mocker.Mock()
    mock_token.token="abc789"

    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    with pytest.raises(HTTPException) as testException: validate_token_service(mock_token)
    assert testException.value.status_code ==401
    
def test_get_user_from_session(mocker,mock_user_response,mock_sessions):
    """checks that get_user_from_session will return a UserResponse if given a valid session token"""
    
    mock_token = {
        "token": "abc456",
        "userid": "1",
        "role": "CUSTOMER",
        "created": "2026-02-20T12:34:56+00:00",
        "expires": "2026-03-20T12:34:56+00:00",
        }
    
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    mocker.patch("app.services.session_manager_service.validate_token_service", return_value = mock_token)    
    mocker.patch("app.services.session_manager_service.get_user_by_id_service", return_value = mock_user_response)
    result = get_user_from_session(Token(token = "abc456"))
        
    assert result.id == "1"
    assert result.role == UserRole.CUSTOMER

def test_get_session_from_token_success(mocker,mock_sessions):
    """tests that get_session_from_token will return a Response given a valid token"""
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    result = get_session_from_token("abc123")
    assert result.token == "abc123"
    assert result.user_id == "1"
    assert result.role == UserRole.CUSTOMER
    
def test_get_session_from_token_success(mocker,mock_sessions):
    """tests that get_session_from_token will return an error if given an invalid token"""
    mocker.patch("app.services.session_manager_service.load_sessions", return_value = mock_sessions)
    with pytest.raises(HTTPException) as testException: get_session_from_token("notoken")
    assert testException.value.status_code ==401