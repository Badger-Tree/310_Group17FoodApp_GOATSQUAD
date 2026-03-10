from pydantic import BaseModel, EmailStr

from app.schemas.Role import UserRole
    
class Token(BaseModel):
    token: str
    
class TokenResponse(BaseModel):
    token:str
    email: EmailStr
    user_id : str
    user_role : UserRole