from datetime import datetime
from pydantic import BaseModel
from app.schemas.Role import UserRole
    
class Token(BaseModel):
    """Base class for token"""
    token: str
    
class TokenResponse(BaseModel):
    """This sends back information about a session/token"""
    token:str
    user_id: str
    role : UserRole
    created : datetime
    expires : datetime