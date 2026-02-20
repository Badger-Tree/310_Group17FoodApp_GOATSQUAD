import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from app.repositories.users_repo import load_all as load_users, save_all as save_all_users
from app.repositories.addresses_repo import load_all  as load_addresses
from app.schemas.Address import AddressResponse
from app.schemas.User import CustomerCreate, CustomerUpdate, CustomerResponse, UserResponse, StaffResponse, StaffCreate, StaffUpdate
from datetime import datetime

# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
def list_users() -> List[UserResponse]:
    user_data = load_users()
    user_responses = []
    for user in user_data:
        user_responses.append(UserResponse(**user))
    return user_responses
                    
def get_user_by_id_service(userid : str) -> CustomerResponse:
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

def register_customer_service(payload: CustomerCreate) -> CustomerResponse:
    users = load_users()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in users):
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    new_user = {"id":new_id, 
                "email":payload.email.strip(), 
                "first_name":payload.first_name.strip(), 
                "last_name" : payload.last_name.strip(), 
                "password" : payload.password.strip(), 
                "role" : ["CUSTOMER"],
                "saved_addresses" : [],
                "created_date": datetime.now(datetime.timezone.utc)}
    users.append(new_user)
    save_all_users(users)
    return CustomerResponse(**new_user)

def register_staff_service(payload: StaffCreate) -> StaffResponse:
    users = load_users()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in users):
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    new_user = {"id":new_id, 
                "email":payload.email.strip(), 
                "first_name":payload.first_name.strip(), 
                "last_name" : payload.last_name.strip(), 
                "password" : payload.password.strip(), 
                "role" : ["STAFF"],
                "created_date": datetime.now(datetime.timezone.utc)}
    users.append(new_user)
    save_all_users(users)
    return StaffResponse(**new_user)


def update_customer_service(userid: str, payload: CustomerUpdate) -> CustomerResponse:
    users = load_users()
    updated = None
    for index, user in enumerate(users):
        if user.get("id") == userid and "CUSTOMER" in user.get("role", []):
            updated =  {"id":userid, 
                "email":user.get("email"), 
                "first_name":payload.first_name.strip() if payload.first_name else user.get("first_name"), 
                "last_name" : payload.last_name.strip()if payload.last_name else user.get("last_name"),
                "password" : payload.password.strip() if payload.password else user.get("password"),
                "role" : user.get("role",["CUSTOMER"]),
                "saved_addresses" : user.get("saved_addresses"),
                "created_date": user.get("created_date")}
            users[index] = updated
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")
    save_all_users(users)
    return CustomerResponse(**updated)
        
    
def update_staff_service(userid: str, payload: StaffUpdate) -> StaffResponse:
    users = load_users()
    updated = None
    for index, user in enumerate(users):
        if user.get("id") == userid and "STAFF" in user.get("role", []):
            updated =  {"id":userid, 
                "email":user.get("email"), 
                "first_name":payload.first_name.strip() if payload.first_name else user.get("first_name"), 
                "last_name" : payload.last_name.strip()if payload.last_name else user.get("last_name"),
                "password" : payload.password.strip() if payload.password else user.get("password"),
                "role" : user.get("role"),
                "created_date": user.get("created_date")}
            users[index] = updated
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")
    save_all_users(users)
    return CustomerResponse(**updated)