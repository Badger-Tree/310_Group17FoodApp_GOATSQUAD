from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.Role import UserRole
    
class Token(BaseModel):
    token: str
    
class TokenResponse(BaseModel):
    """This sends a token response back to API"""
    token:str
    user_id: str
    role : UserRole
    created : datetime
    expires : datetime