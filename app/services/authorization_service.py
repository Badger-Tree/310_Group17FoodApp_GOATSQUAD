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
    """Used to check if a user has a specific role (singular) and raises forbidden exception if not. 
    Input: UserResponse.
    Output: none"""
    if user.role != role:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
def require_role_multi_service(user: UserResponse, roles: list[UserRole]):
    """Used to check if a user has a specific role from a list and raises forbidden exception if not. 
    Input: a list of UserResponse.
    Output: none"""
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="Unauthorized")