from fastapi import APIRouter, status
from typing import List
from app.schemas.Address import AddressResponse, AddressCreate, AddressUpdate
from app.services.address_service import get_address_by_id_service, get_address_by_customer_id_service, create_address_service, update_address_service, delete_address_service


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

@router.post("", response_model=AddressResponse, status_code=201)
def create_address(payload: AddressCreate):
    """Creates and saves a new address associated with a customer account
    Intake: AddressCreate as payload(street, city, postal_code, instructions,user_id)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    return create_address_service(payload)

@router.put("/update/{addressid}", response_model=AddressResponse)
def update_address(addressid: str, payload: AddressUpdate):
    """Updates the street, city, postal_code, and/or instructions for an address
    Intake: AddressUpdate as payload (street, city, postal_code, instructions)
    Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
    return update_address_service(addressid, payload)

@router.delete("/delete/{addressid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(addressid:str):
    """Delets a saved address
    Intake: Address id as string
    Return: None"""
    delete_address_service(addressid)
    return None