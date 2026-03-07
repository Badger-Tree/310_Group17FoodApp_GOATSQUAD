
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users, save_all as save_all_users
from app.schemas.User import UserResponse, UserUpdate
from app.factories.user_factory import CustomerFactory, StaffFactory, CustomerCreate, StaffCreate
from app.schemas.Role import UserRole


# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
def list_users() -> List[UserResponse]:
    """This function returns a list of UserResponse objects for all users in system"""
    user_data = load_users()
    user_responses = []
    for user in user_data:  
        user_responses.append(UserResponse(**user))
    if not user_data: 
        raise HTTPException(status_code=404, detail=f"No registed users")
    return user_responses
                    
def get_user_by_id_service(userid : str) -> UserResponse:
    """This function returns a UserResponse for a user given a user id"""
    user_data = load_users()
    for u in user_data: 
        if u.get("id") == userid:
            return UserResponse(**u)
    raise HTTPException(status_code=404, detail=f"User '{userid}' not found")

def get_user_by_email_service(email: str) -> UserResponse:
    """This function returns a UserResponse for a user given a user's email address"""
    user_data = load_users()
    for u in user_data:
        if u.get("email").lower() == email.lower():
            return UserResponse(**u)
    raise HTTPException(status_code=404, detail=f"User '{email}' not found")

def register_user_service(payload: CustomerCreate | StaffCreate, role: UserRole) -> UserResponse:
    """This function creates an account for a user as staff or customer"""
    users = load_users()
    for user in users:
        if user["email"].lower() == payload.email.strip().lower():
            raise HTTPException(status_code=409, detail = "Account with that email already exists")
    if role ==UserRole.CUSTOMER:
        factory = CustomerFactory()
    elif role == UserRole.STAFF:
        factory = StaffFactory()
    else:raise HTTPException(status_code=400, detail=f"User role not found")
    new_user = factory.create_user(payload)

    for user in users:
        if user["id"] == new_user["id"]:
            raise HTTPException(status_code=409, detail="ID collision; retry.")
    users.append(new_user)
    save_all_users(users)
    return UserResponse(**new_user)

def update_user_service(userid:str, payload:UserUpdate) -> UserResponse:
    """this function updates a user record in db (csv) with provided first name, last name, and/or password"""
    users = load_users()
    updated = None
    for index, user in enumerate(users):
        if user.get("id") == userid:
            updated = {"id":userid, 
                "email" : user.get("email"),
                "first_name":payload.first_name.strip() if payload.first_name else user.get("first_name"), 
                "last_name" : payload.last_name.strip()if payload.last_name else user.get("last_name"),
                "password" : payload.password.strip() if payload.password else user.get("password"),
                "role" : user.get("role"),
                "created_date": user.get("created_date"),
                }
            users[index] = updated
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")
    save_all_users(users)
    return UserResponse(**updated)