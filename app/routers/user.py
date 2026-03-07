from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.User import CustomerCreate, UserResponse, StaffCreate, UserUpdate
from app.schemas.Role import UserRole
from app.services.user_service import list_users, get_user_by_id_service, get_user_by_email_service, register_user_service, update_user_service


router = APIRouter(prefix="/users", tags=["users"])

# this method (showing all users) is just for testing, doesn't have a role in
# the actual project architecture
#further note that all methods / data relating to Roles needs to be updated after Role is built as a class
@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users():
    users = list_users()
    return users

@router.get("/{userid}", response_model=UserResponse)
def get_user_by_id(userid: str):
    return get_user_by_id_service(userid)

@router.get("/by-email/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    return get_user_by_email_service(email)

@router.post("/new-customer", response_model=UserResponse, status_code=201)
def register_customer(payload: CustomerCreate):
    return register_user_service(payload, role=UserRole.CUSTOMER)

@router.post("/new-staff", response_model=UserResponse, status_code=201)
def register_staff(payload: StaffCreate):
    return register_user_service(payload, role=UserRole.STAFF)

@router.put("/update-user/{userid}", response_model=UserResponse)
def update_user(userid: str, payload: UserUpdate):
    return update_user_service(userid, payload)
