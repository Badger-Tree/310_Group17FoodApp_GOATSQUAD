from pydantic import ValidationError
from datetime import datetime
import pytest
from app.schemas.Address import Address, AddressCreate, AddressUpdate, AddressResponse

def test_Address_success():
    """test that Address is created successfully with valid data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5",
                  "instructions": "leave at door"}
    result = Address(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at door"

def test_Address_partial_input():
    """test that Address is created successfully without optional data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5"}
    result = Address(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == None
    
def test_Address_invalid_input():
    """test that Address creates an error if it receives invalid input"""
    input_data = {"street":"",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5"}
    with pytest.raises(ValidationError): Address(**input_data)
    
def test_Address_missing_input():
    """test that Address creates an error if it receives incomplete input"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough"}
    with pytest.raises(ValidationError): Address(**input_data)
    
def test_AddressCreate_success():
    """test that AddressCreate is created successfully with valid data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5",
                  "instructions": "leave at door"}
    result = Address(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at door"
    
def test_AddressCreate_success_partial_input():
    """test that AddressCreate is created successfully without optional data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5"}
    result = Address(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == None
    
def test_AddressUpdate_success():
    """tests that AddressUpdate creates successfully with valid input"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5",
                  "instructions": "leave at side door"}
    result = AddressUpdate(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at side door"


# def test_Address_update_empty():
    """test that AddressUpdate can be created given no input"""
    input_data = {}
    result = AddressUpdate(**input_data)
    assert result.street == None
    assert result.city == None
    assert result.postal_code == None
    assert result.instructions == None


# def test_AddressUpdate_partial_input():
    """test that AddressUpdate can be created given partial input data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough"}
    result = AddressUpdate(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == None
    assert result.instructions == None
    
def test_AddressUpdate_invalid_input():
    """test that AddressUpdate generates a validation error if given an invalid input"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "",
                  "postal_code":"H0B 1T5"}
    with pytest.raises(ValidationError): AddressUpdate(**input_data)
    
# def test_AddressResponse_success():
    """test that AddressResponse is created successfully with valid data"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5",
                  "instructions": "leave at side door",
                  "address_id": "1234",
                  "user_id": "5678",
                  "created_date": "2023-02-20T12:34:56"}
    result = AddressResponse(**input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at side door"
    assert result.address_id == "1234"
    assert result.user_id == "5678"
    assert result.created_date == datetime.fromisoformat("2023-02-20T12:34:56")
    
def test_AddressResponse_invalid_input():
    """test that AddressResponse raises validation exception if not given valid input"""
    input_data = {"street":"123 Brandybuck Lane",
                  "city": "Tuckburough",
                  "postal_code":"H0B 1T5",
                  "instructions": "leave at side door",
                  "address_id": "1234",
                  "user_id": 1234,
                  "created_date": "2023-02-20T12:34:56"}
    with pytest.raises(ValidationError): AddressResponse(**input_data)