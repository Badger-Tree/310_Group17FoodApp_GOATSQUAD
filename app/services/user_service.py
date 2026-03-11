
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users, save_all as save_all_users
from app.schemas.User import UserResponse, UserUpdate
from app.factories.user_factory import CustomerFactory, StaffFactory
from app.schemas.Role import UserRole


# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
def list_users() -> List[UserResponse]:
    user_data = load_users()
    user_responses = []
    for user in user_data:  
        user_responses.append(UserResponse(**user))
    return user_responses
                    
def get_user_by_id_service(userid : str) -> UserResponse:
    user_data = load_users()
    for u in user_data: 
        if u.get("id") == userid:
            return UserResponse(**u)
    raise HTTPException(status_code=404, detail=f"User '{userid}' not found")

def get_user_by_email_service(email: str) -> UserResponse:
    user_data = load_users()
    for u in user_data:
        if u.get("email").lower() == email.lower():
            return UserResponse(**u)
    raise HTTPException(status_code=404, detail=f"User '{email}' not found")

def register_user_service(payload, role: UserRole) -> UserResponse:
    users = load_users()
    if role ==UserRole.CUSTOMER:
        factory = CustomerFactory()   
    elif role == UserRole.STAFF:
        factory = StaffFactory()
    else:raise HTTPException(status_code=400, detail=f"User role not found")
    new_user = factory.create_user(payload)
    if any(it.get("id") == new_user["id"] for it in users):
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    users.append(new_user)
    save_all_users(users)
    return UserResponse(**new_user)

def update_user_service(userid:str, payload:UserUpdate, role:UserRole) -> UserResponse:
    users = load_users()
    updated = None
    for index, user in enumerate(users):
        if user.get("id") == userid:
            updated = {"id":userid, 
                "email":user.get("email"), 
                "first_name":payload.first_name.strip() if payload.first_name else user.get("first_name"), 
                "last_name" : payload.last_name.strip()if payload.last_name else user.get("last_name"),
                "password" : payload.password.strip() if payload.password else user.get("password"),
                "role" : role,
                "created_date": user.get("created_date")}
            users[index] = updated
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")
    save_all_users(users)
    return UserResponse(**updated)