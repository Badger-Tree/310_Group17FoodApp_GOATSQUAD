from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import secrets
from app.schemas.Login import LoginRequest
from app.schemas.Token import Token, TokenResponse
from app.repositories.sessions_repo import load_all as load_sessions, save_all as save_sessions
from app.schemas.User import UserResponse
from app.services.user_service import get_user_by_email_service, get_user_by_id_service

def create_session_service(email) -> TokenResponse:
    """Creates and stores a session. 
    Input:user email (str). 
    Output: TokenResponse (userid, token, created, expires) """
    token = secrets.token_hex(16)
    created = datetime.now(timezone.utc)
    expires = created + timedelta(hours=1)

    user = get_user_by_email_service(email)
    sessions = load_sessions()
    sessions.append({"userid":user.id,
                     "role":user.role,
                     "token": token,
                     "created" : created.isoformat(),
                     "expires" : expires.isoformat()})
    save_sessions(sessions)
    
    new_token = {"token": token,
                "user_id": user.id,
                "role" : user.role,
                "created" : created,
                "expires" : expires}
    sessions = load_sessions()
    return TokenResponse(**new_token)

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

def get_user_from_session(token: Token) -> UserResponse:
    """gets a userid from the session token and returns the corresponding UserResponse"""
    session = validate_token_service(token)
    user = get_user_by_id_service(session["userid"])
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

def get_session_from_token(token:str):
    """returns a full token response (token, user id, role, created, expires) from the token"""
    sessions = load_sessions()
    for session in sessions:
        if session["token"] == token:
            return TokenResponse(token = session["token"],
                                 user_id = session["user_id"],
                                role = session["role"],
                                created = session["created"],
                                expires = session["expires"])
    raise HTTPException(status_code=401, detail="invalid token")