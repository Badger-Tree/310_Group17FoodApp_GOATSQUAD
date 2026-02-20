import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from app.repositories.users_repo import load_all as load_users
from app.repositories.addresses_repo import load_all  as load_addresses, save_all as save_addresses
from app.schemas.Address import AddressCreate, AddressResponse, AddressUpdate
from datetime import datetime

def get_address_by_id_service(address_id: str) -> AddressResponse:
    addresses_data = load_addresses()
    for a in addresses_data:
        if a.get("address_id") == address_id:
            return AddressResponse(**a)
    raise HTTPException(status_code=404, detail=f"Address '{address_id}' not found")

def get_address_by_customer_id_service(customer_id: str) -> List[AddressResponse]:
    addresses_data = load_addresses()
    address_responses = []
    
    for a in addresses_data:
        if a.get("user_id") == customer_id:
            address_responses.append(AddressResponse(**a))
    if not address_responses:
        raise HTTPException(status_code=404, detail=f"Customer '{customer_id}' not found")
    return address_responses
    
def create_address_service(payload: AddressCreate) -> AddressResponse:
    addresses_data = load_addresses()
    new_id = str(uuid.uuid4())
    if any(it.get("address_id") == new_id for it in addresses_data):
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    
    ##check if the user id exists else we can't add to a user
    users = load_users()
    user_exists = False
    for u in users:
        if u["id"] == payload.user_id.strip():
            user_exists = True
            break
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User {payload.user_id} not found")

    new_address = {
        "address_id" : new_id,
        "user_id" : payload.user_id.strip(),
        "street": payload.street.strip(),
        "city": payload.city.strip(),
        "postal_code": payload.postal_code.strip(),
        "instructions": payload.instructions.strip(),
        "created_date": datetime.utcnow().isoformat()
    }
    addresses_data.append(new_address)
    save_addresses(addresses_data)
    return AddressResponse(**new_address) 
    


def update_address_service(addressid: str, payload: AddressUpdate) -> AddressResponse:
    addresses_data = load_addresses()
    updated = None
    for index, address in enumerate(addresses_data):
        if address.get("address_id")==addressid:
            updated = { "address_id" : addressid,
                        "user_id" : address.get("user_id"),
                        "street": payload.street.strip() if payload.street else address.get("street"),
                        "city": payload.city.strip() if payload.city else address.get("city"),
                        "postal_code": payload.postal_code.strip() if payload.postal_code else address.get("postal_code"),
                        "instructions": payload.instructions.strip()if payload.instructions else address.get("instructions"),
                        "created_date": address.get("created_date")}
            addresses_data[index] = updated
            break
    if not updated:
        raise HTTPException(status_code=404, detail=f"Address {addressid} not found")
    save_addresses(addresses_data)
    return AddressResponse(**updated)

def delete_address_service(addressid:str) -> None:
    addresses_data = load_addresses()
    found_address = False
    for index, address in enumerate(addresses_data):
        if address.get("address_id") == addressid:
            found_address = True
            addresses_data.pop(index)
            break
    if not found_address:
        raise HTTPException(status_code=404, detail=f"Address {addressid} not found")
    save_addresses(addresses_data)
        