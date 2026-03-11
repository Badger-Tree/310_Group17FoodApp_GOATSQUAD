from fastapi import APIRouter, HTTPException, Header, status
from typing import List
from app.schemas.User import CustomerCreate, UserResponse, StaffCreate, UserUpdate
from app.schemas.Role import UserRole
from app.services.user_service import  get_user_by_id_service, get_user_by_email_service, register_user_service, update_user_service


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{userid}", response_model=UserResponse)
def get_user_by_id(userid: str):
    """Finds a user given a user id
    Intake: userid (str)
    Return: UserResponse (email, first_name, last_name, id, role, created_date)"""
    return get_user_by_id_service(userid)

@router.get("/by-email/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    """Finds a user given a email (str)
    Intake: email (str)
    Return: UserResponse (email, first_name, last_name, id, role, created_date)"""
    return get_user_by_email_service(email)

@router.post("/new-customer", response_model=UserResponse, status_code=201)
def register_customer(payload: CustomerCreate):
    """registers a new user as a customer with UserRole CUSTOMER
    Intake: CustomerCreate object as payload (email, first_name, last_name, password)
    Return: UserResponse (email, first_name, last_name, id, role, created_date)"""
    return register_user_service(payload, role=UserRole.CUSTOMER)

@router.post("/new-staff", response_model=UserResponse, status_code=201)
def register_staff(payload: StaffCreate):
    """registers a new user as staff with UserRole STAFF
    Intake: StaffCreate object as payload (email, first_name, last_name, password)
    Return: UserResponse (email, first_name, last_name, id, role, created_date)"""
    return register_user_service(payload, role=UserRole.STAFF)

@router.put("/update-user/{userid}", response_model=UserResponse)
def update_user(payload: UserUpdate, token: str = Header(...)):
    """Updates the first_name, last_name, and/or password for an account. 
    Intake: userid, UserUpdate as payload
    Return: UserResponse (email, first_name, last_name, id, role, created_date)"""
    session = Token(token=token)
    user = get_user_from_session(session)
    
    
    return update_user_service(userid, payload)
