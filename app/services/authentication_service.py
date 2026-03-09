from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users
import secrets
from app.schemas.Login import LoginRequest, LoginResponse, TokenResponse
from app.services.user_service import get_user_by_email_service, get_user_by_id_service

def login_service(credentials: LoginRequest) -> LoginResponse:
    user = get_user_by_email_service(credentials.email)
    if not user or user.get("password") != credentials.password:
        raise HTTPException(status_code=401, detail=f"Incorrect credentials")
    token = create_token(user.get("id"))
    return LoginResponse(token = token, user_id=user.get("id"),user_role=user.get("role"))
    

sessions = {}

def create_token(userid: str) -> str:
    token = secrets.token_hex(16)
    created = datetime.utcnow()
    expires = created + timedelta(hours=1)
    # add session to sessions csv
    
    return token

def get_user_from_token_service(token: str) -> TokenResponse:
    userid = sessions.get(token)
    if not userid:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id_service(userid)
    return TokenResponse(token=token,
                         email=user.get("email"), 
                         user_id = user.get("id"), 
                         role = user.get("role"))