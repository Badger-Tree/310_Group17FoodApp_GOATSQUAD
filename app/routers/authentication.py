from fastapi import APIRouter, status
from app.schemas.Session import LoginRequest, LoginResponse
from app.services.authentication_service import login_service, get_user_from_token_service, logout_service
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    return login_service(credentials)
    
def helper_get_user_from_token(token:str):
    return get_user_from_token_service(token)

@router.post("/logout")
def logout(token:str):
    return logout_service(token)