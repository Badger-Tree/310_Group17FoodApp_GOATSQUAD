from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.schemas.Role import UserRole
from app.services.session_manager_service import create_session_service, expire_session_service
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

# def test_expire_session_service(mocker):
#     """tests that expire_session_service will remove a session record given a token (str)"""
#     mock_token = "abc123"
        
#     mock_sessions = [
#         {"token": "abc123", "user_id": "1"},
#         {"token": "def456", "user_id": "2"}
#         ]
    
#     def mock_load_sessions():
#         return mock_sessions

#     def mock_save_sessions():
#         return []
#     mocker.patch("app.services.session_manager_service.load_sessions", mock_load_sessions())
#     mocker.patch("app.services.session_manager_service.save_sessions", mock_save_sessions())

#     result = expire_session_service(mock_token)
#     assert result is None

    
# def test_validate_token_service_success

# def test_validate_token_service_session_not_found

    
# def test_validate_token_service_session_expired