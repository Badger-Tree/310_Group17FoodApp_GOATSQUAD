from fastapi import APIRouter, status
from typing import List
from app.schemas.User import CustomerCreate, CustomerUpdate, CustomerResponse, UserResponse, StaffResponse, StaffCreate, StaffUpdate
from app.services.user_service import list_users, get_user_by_id_service, get_user_by_email_service, register_customer_service, update_customer_service, update_staff_service, register_staff_service



router = APIRouter(prefix="/users", tags=["users"])


# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
#further note that all methods / data relating to Roles needs to be updated after Role is built as a class
@router.get("", response_model=List[CustomerResponse], status_code=status.HTTP_200_OK)
def get_users():
    customers = list_users()
    return customers

@router.get("/{userid}", response_model=CustomerResponse)
def get_user_by_id(userid: str):
    return get_user_by_id_service(userid)

@router.get("/by-email/{email}", response_model=CustomerResponse)
def get_user_by_email(email: str):
    return get_user_by_email_service(email)

@router.post("/new-customer", response_model=CustomerResponse, status_code=201)
def register_customer(payload: CustomerCreate):
    return register_customer_service(payload)

@router.put("/update-customer/{userid}", response_model=CustomerResponse)
def update_user(userid: str, payload: CustomerUpdate):
    return update_customer_service(userid, payload)

@router.post("/new-staff", response_model=StaffResponse, status_code=201)
def register_staff(payload: StaffCreate):
    return register_staff_service(payload)

@router.put("/update-staff/{userid}", response_model=StaffResponse)
def update_user(userid: str, payload: StaffUpdate):
    return update_staff_service(userid, payload)