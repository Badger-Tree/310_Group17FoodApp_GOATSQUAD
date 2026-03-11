from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import secrets
from app.schemas.Login import LoginRequest
from app.schemas.Token import Token, TokenResponse
from app.repositories.sessions_repo import load_all as load_sessions, save_all as save_sessions
from app.services.user_service import get_user_by_email_service

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

def expire_session_service(token:str): 
    sessions = load_sessions()
    new_sessions = []
    for session in sessions:
        if session["token"] != token:
            new_sessions.append(session)
    if len(new_sessions) == len(sessions):
        raise HTTPException(status_code=401, detail="invalid token")
    save_sessions(new_sessions)

def validate_token_service(token: Token) -> dict:
    sessions = load_sessions()
    for session in sessions:
        if session["token"] == token.token:
            expires = datetime.fromisoformat(session["expires"])
            if datetime.now(timezone.utc) > expires:
                expire_session_service(token)
                raise HTTPException(status_code=401, detail="session expired")
            return (session)
    raise HTTPException(status_code=404, detail="session not found")