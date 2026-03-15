from fastapi import APIRouter, Header, status
from typing import List
from app.schemas.Address import AddressResponse, AddressCreate, AddressUpdate
from app.services.address_service import get_address_by_id_service, get_address_by_customer_id_service, create_address_service, update_address_service, delete_address_service
from app.schemas.Token import Token
from app.services.session_manager_service import get_user_from_session, validate_token_service

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/by-id/{address_id}", response_model=AddressResponse)
def get_address_by_id(address_id: str):
    """Finds an address given an address id (str)
    Intake: address_id (str)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    return get_address_by_id_service(address_id)

@router.get("/by-customer/{customer_id}", response_model=List[AddressResponse])
def  get_address_by_customer_id(customer_id: str):
    """Finds an address given a customer's user id
    Intake: userid (str)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    return get_address_by_customer_id_service(customer_id)

@router.post("/new", response_model=AddressResponse, status_code=201)
def create_address(payload: AddressCreate, token: str = Header(...)):
    """Creates and saves a new address associated with a customer account
    Intake: AddressCreate as payload(street, city, postal_code, instructions,user_id)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    return create_address_service(payload, current_user_id)

@router.put("/update/{addressid}", response_model=AddressResponse)
def update_address(addressid: str, payload: AddressUpdate,token: str = Header(...)):
    """Updates the street, city, postal_code, and/or instructions for an address
    Intake: AddressUpdate as payload (street, city, postal_code, instructions)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    session = Token(token=token)
    if validate_token_service(session) is not None:
        return update_address_service(addressid, payload)

@router.delete("/delete/{addressid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(addressid:str,token: str = Header(...)):
    """Delets a saved address
    Intake: Address id as string
    Return: None"""
    session = Token(token=token)
    if validate_token_service(session) is not None:
        delete_address_service(addressid)
        return None


