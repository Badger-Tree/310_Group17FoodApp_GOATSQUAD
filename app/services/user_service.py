import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from app.repositories.users_repo import load_all as load_users, save_all as save_all_users
from app.repositories.addresses_repo import load_all  as load_addresses
from app.schemas.Address import AddressResponse
from app.schemas.User import CustomerCreate, CustomerUpdate, CustomerResponse
from datetime import datetime

# this method (showing all customers) is just for testing, doesn't have a role in
# the actual project architecture
def list_customers() -> List[CustomerResponse]:
    customers_data = load_users()
    customer_responses = []
    for user in customers_data:
        role_list = user.get("role")
        if role_list is not None and "CUSTOMER" in role_list:
            customer_responses.append(CustomerResponse(**user))
    return customer_responses
                    
def get_user_by_id_service(userid : str) -> CustomerResponse:
    customers_data = load_users()
    for c in customers_data: 
        if c.get("id") == userid:
            return CustomerResponse(**c)
    raise HTTPException(status_code=404, detail=f"Customer '{customer_id}' not found")

def get_customer_by_email_service(email: str) -> CustomerResponse:
    customers_data = load_users()
    addresses_data = load_addresses()
    for c in customers_data:
        if c.get("email").lower() == email.lower() and "CUSTOMER" in c.get("role", []):
            user_addresses = [AddressResponse(**a) for a in addresses_data if a.get("user_id") == c.get("id")]
            return CustomerResponse(**c, saved_addresses=user_addresses)
    raise HTTPException(status_code=404, detail=f"Customer '{email}' not found")

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

def update_customer_service(userid: str, payload: CustomerUpdate) -> CustomerResponse:
    users = load_users()
    updated = None
    for index, user in enumerate(users):
        if user.get("id") == userid:
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
        