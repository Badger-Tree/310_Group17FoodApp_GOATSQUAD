from fastapi import HTTPException

from app.schemas.Role import UserRole
from app.schemas.User import UserResponse

def has_role_service(user: UserResponse, role: UserRole) -> bool:
    """Used to check if a user has a specific role. 
    Input: UserResponse.
    Output: boolean"""
    if user.role == role:
        return True
    else:
        return False

def require_role_service(user: UserResponse, role: UserRole):
    """Used to check if a user has a specific role and raises forbidden exception if not. 
    Input: UserResponse.
    Output: none"""
    if user.role != role:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    