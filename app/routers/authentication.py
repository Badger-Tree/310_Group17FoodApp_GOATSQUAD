from fastapi import APIRouter, status
from app.schemas.Login import LoginRequest, LoginResponse
from app.services.authentication_service import login_service, get_user_from_token_service
router = APIRouter(prefix="/login", tags=["login"])

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    return login_service(credentials)
    
def helper_get_user_from_token(token:str):
    get_user_from_token_service(token)