from pydantic import BaseModel, EmailStr

from app.schemas import Role

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    user_id : str
    user_role : Role
    
class Token(BaseModel):
    token: str
    
class TokenResponse(BaseModel):
    token:str
    email: EmailStr
    user_id : str
    user_role : Role