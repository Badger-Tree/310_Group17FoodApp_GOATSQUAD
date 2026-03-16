from fastapi import APIRouter, Header, status
from app.schemas.Login import LoginRequest
from app.schemas.Token import Token, TokenResponse

from app.services.authentication_service import login_service, logout_service
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Lets user log into system. 
    Input: LoginRequest(email, password). 
    Output: TokenResponse (token, email, user_id, UserRole)"""
    return login_service(credentials)
    
@router.post("/logout")
def logout(token: str = Header(...)):
    """Lets a user log out of the service. Input: Token. Output: dict"""
    session = Token(token=token)
    return logout_service(session)