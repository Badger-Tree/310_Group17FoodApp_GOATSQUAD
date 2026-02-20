from fastapi import APIRouter, status
from typing import List
from app.schemas.User import CustomerResponse, CustomerCreate, CustomerUpdate
from app.services.user_service import list_customers, get_customer_by_id_service, get_customer_by_email_service, register_customer_service, update_customer_service


router = APIRouter(prefix="/users", tags=["users"])


# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
#further note that all methods / data relating to Roles needs to be updated after Role is built as a class
@router.get("", response_model=List[CustomerResponse], status_code=status.HTTP_200_OK)
def get_customers():
    customers = list_customers()
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: str):
    return get_customer_by_id_service(customer_id)

@router.get("/by-email/{email}", response_model=CustomerResponse)
def get_customer_by_email(email: str):
    return get_customer_by_email_service(email)

@router.post("", response_model=CustomerResponse, status_code=201)
def register_user(payload: CustomerCreate):
    return register_customer_service(payload)

@router.put("/update/{userid}", response_model=CustomerResponse)
def update_user(userid: str, payload: CustomerUpdate):
    return update_customer_service(userid, payload)