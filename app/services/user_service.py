
from typing import List
from fastapi import HTTPException
from app.repositories.users_repo_csv import find_by_email_repo, find_by_id_repo, find_by_email_repo, add_user_repo, update_user_repo
from app.schemas.User import UserResponse, UserUpdate
from app.factories.user_factory import CustomerFactory, StaffFactory, CustomerCreate, StaffCreate
from app.schemas.Role import UserRole
from app.services.cart_service import create_cart

def get_user_by_id_service(userid : str) -> UserResponse:
    """This function returns a UserResponse for a user given a user id"""
    user = find_by_id_repo(userid)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{userid}' not found")    
    return UserResponse(**user)

def get_user_by_email_service(email: str) -> UserResponse:
    """This function returns a UserResponse for a user given a user's email address"""
    user = find_by_email_repo(email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{email}' not found") 
    return UserResponse(**user)

def register_user_service(payload: CustomerCreate | StaffCreate, role: UserRole) -> UserResponse:
    """This function creates an account for a user as staff or customer"""
    if find_by_email_repo(payload.email):
        raise HTTPException(status_code=409, detail = "Account with that email already exists")
    if role ==UserRole.CUSTOMER:
        factory = CustomerFactory()
    elif role == UserRole.STAFF:
        factory = StaffFactory()
    else:raise HTTPException(status_code=400, detail=f"User role not found")
    new_user = factory.create_user(payload)
    new_user = add_user_repo(new_user)
    if role == UserRole.CUSTOMER:
        create_cart(new_user["id"])
    return UserResponse(**new_user)

def update_user_service(user_id:str, payload:UserUpdate) -> UserResponse:
    """this function updates a user record in db (csv) with provided first name, last name, and/or password"""
    updated_fields = {}
    if payload.first_name is not None:
        updated_fields["first_name"] = payload.first_name.strip()
    if payload.last_name is not None:
        updated_fields["last_name"] = payload.last_name.strip()
    if payload.password is not None:
        updated_fields["password"] = payload.password.strip()
    if not updated_fields:
        raise HTTPException(status_code=400, detail=f"nothing to update")
    updated_user = update_user_repo(user_id, updated_fields)
    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserResponse(**updated_user)