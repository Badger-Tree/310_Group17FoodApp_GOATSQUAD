from fastapi import APIRouter, status
from typing import List
from app.schemas.Address import AddressResponse, AddressCreate, AddressUpdate
from app.services.address_service import get_address_by_id_service, get_address_by_customer_id_service, create_address_service, update_address_service, delete_address_service


router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/by-id/{address_id}", response_model=AddressResponse)
def get_address_by_id(address_id: str):
    """function gets an address object (AddressResponse) given an address id"""
    return get_address_by_id_service(address_id)

@router.get("/by-customer/{customer_id}", response_model=List[AddressResponse])
def  get_address_by_customer_id(customer_id: str):
    """function gets a list of address objects (AddressResponse) given a customer id"""
    return get_address_by_customer_id_service(customer_id)

@router.post("", response_model=AddressResponse, status_code=201)
def create_address(payload: AddressCreate, userid: str):
    """function creates an address given an AddressCreate payload"""
    return create_address_service(payload, userid)

@router.put("/update/{addressid}", response_model=AddressResponse)
def update_address(addressid: str, payload: AddressUpdate):
    """function updates an address given an AddressUpdate payload"""
    return update_address_service(addressid, payload)

@router.delete("/delete/{addressid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(addressid:str):
    """function deletes an address object given an address id"""
    delete_address_service(addressid)
    return None