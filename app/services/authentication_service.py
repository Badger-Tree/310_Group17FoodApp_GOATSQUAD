from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users
import secrets
from app.schemas.Session import LoginRequest, LoginResponse, TokenResponse
from app.services.user_service import get_user_by_email_service, get_user_by_id_service
from app.repositories.sessions_repo import load_all as load_sessions, save_all as save_sessions
from app.repositories.users_repo_csv import load_all as load_users

def login_service(credentials: LoginRequest) -> LoginResponse:
    users = load_users()
    for user in users:
        if user["email"] == credentials.email:
            if user["password"] != credentials.password:
                raise HTTPException(status_code=401, detail=f"Incorrect credentials")
            token = create_token(user["id"])
            return LoginResponse(token = token, 
                                 user_id=user["id"],
                                 user_role=user["role"])
    raise HTTPException(status_code=401, detail=f"Incorrect credentials")

def create_token(userid: str) -> str:
    token = secrets.token_hex(16)
    created = datetime.now(timezone.utc)
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
            expires = datetime.fromisoformat(session["expires"])
            if datetime.now(timezone.utc) > expires:
                raise HTTPException(status_code=401, detail="session expired")
            user = get_user_by_id_service(session.userid)
            return TokenResponse(token=token,
                         email=user.email, 
                         user_id = user.id, 
                         role = user.role)
    raise HTTPException(status_code=401, detail="invalid token")

def logout_service(token:str):
    sessions = load_sessions()
    new_sessions = []
    for session in sessions:
        if session["token"] != token:
            new_sessions.append(session)
        if len(new_sessions) == len(sessions):
            #this means nothing was deleted
            raise HTTPException(status_code=401, detail="invalid token")
    save_sessions(new_sessions)
    return {"detail" : "logout successful"}