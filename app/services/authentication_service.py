from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users
import secrets
from app.schemas.Login import LoginRequest, LoginResponse, TokenResponse
from app.services.user_service import get_user_by_email_service, get_user_by_id_service
from app.repositories.sessions_repo import load_all as load_sessions, save_all as save_sessions

def login_service(credentials: LoginRequest) -> LoginResponse:
    user = get_user_by_email_service(credentials.email)
    if not user or user.get("password") != credentials.password:
        raise HTTPException(status_code=401, detail=f"Incorrect credentials")
    token = create_token(user.get("id"))
    return LoginResponse(token = token, user_id=user.get("id"),user_role=user.get("role"))

def create_token(userid: str) -> str:
    token = secrets.token_hex(16)
    created = datetime.now(datetime.timezone.utc)
    expires = created + timedelta(hours=1)

    sessions = load_sessions()
    sessions.append({"userid":userid,
                     "token": token,
                     "created" : created.isoformat(),
                     "expires" : expires.isoformat()})
    save_sessions(sessions)
    return token

def get_user_from_token_service(token: str) -> TokenResponse:
    sessions = load_sessions()
    for session in sessions:
        if session["token"] == token:
            if datetime.now(datetime.timezone.utc) > session["expires"]:
                raise HTTPException(status_code=401, detail="session expired")
            user = get_user_by_id_service(session.get("userid"))
            return TokenResponse(token=token,
                         email=user.get("email"), 
                         user_id = user.get("id"), 
                         role = user.get("role")
            )
    raise HTTPException(status_code=401, detail="invalid token")

def logout_service(token:str):
    sessions = load_sessions()
    new_sessions = []
    for session in sessions:
        if session["token"] != token:
            new_sessions.append(session)
        if len(new_sessions) == sessions:
            #this means nothing was deleted
            raise HTTPException(status_code=401, detail="invalid token")
    save_sessions(new_sessions)
    return {"detail" : "logout successful"}