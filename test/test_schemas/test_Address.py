from pydantic import ValidationError
from datetime import datetime
import pytest
from app.schemas.Address import Address, AddressCreate, AddressUpdate, AddressResponse

def test_Address_success():
    """test that Address is created successfully with valid data"""

# def test_Address_partial_input():
    """test that Address is created successfully without optional data"""
# def test_Address_invalid_input():
    """test that Address creates an error if it receives in invalid email input"""
    
# def test_Address_invalid_missing_input():
    """test that Address creates an error if it receives incomplete input"""

# def test_AddressCreate_success()
    """test that AddressCreate is created successfully with valid data"""
    
# def test_AddressUpdate_success()
    """tests that AddressUpdate creates successfully with valid input"""

# def test_Address_update_empty():
    """test that AddressUpdate can be created given no input"""

# def test_AddressUpdate_partial_input():
    """test that AddressUpdate can be created given partial input data"""
    
# def test_AddressUpdate_invalid_input():
    """test that AddressUpdate generates a validation error if given an invalid input"""

# def test_AddressResponse_success()
    """test that AddressResponse is created successfully with valid data"""
    
# def test_AddressResponse_invalid_input()
    """test that AddressResponse raises validation exception if not given valid input"""