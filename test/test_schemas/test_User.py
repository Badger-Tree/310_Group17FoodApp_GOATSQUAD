from pydantic import ValidationError
from datetime import datetime

import pytest
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, StaffCreate, UserBase, UserResponse, UserUpdate

def test_user_base_valid():
    """test that UserBase is created successfully with valid data"""
    input_data = {"email":"pippin@shire.me",
                  "first_name": "peregrin",
                  "last_name":"took"}
    result = UserBase(**input_data)
    assert result.email == "pippin@shire.me"
    assert result.first_name == "peregrin"
    assert result.last_name == "took"

def test_user_base_invalid_email():
    """test that UserBase creates an error if it receives in invalid email input"""
    input_data = {"email":"pippinshire.me",
                  "first_name": "peregrin",
                  "last_name":"took"}
    with pytest.raises(ValidationError): UserBase(**input_data)

def test_user_base_missing_fields():
    """test that UserBase creates an error if it receives an input with missing field"""
    input_data = {"email":"pippinshire.me",
                  "last_name":"took"}
    with pytest.raises(ValidationError): UserBase(**input_data)

def test_user_response_valid():
    """test that UserResponse is created successfully with valid data"""
    input_data = {"email":"pippin@shire.me",
                  "first_name": "peregrin",
                  "last_name":"took",
                  "id": "1",
                  "role":"CUSTOMER",
                  "created_date": "2026-02-20T12:34:56"}
    result = UserResponse(**input_data)
    assert result.email == "pippin@shire.me"
    assert result.first_name == "peregrin"
    assert result.last_name == "took"
    assert result.role == UserRole.CUSTOMER
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")
    assert result.id == "1"
    
def test_user_response_invalid_role():
    """test that UserResponse raises validation exception if not given valid user role"""
    input_data = {"email":"pippin@shire.me",
                  "first_name": "peregrin",
                  "last_name":"took",
                  "id": "1",
                  "role":"Customer",
                  "created_date": "2026-02-20T12:34:56"}
    with pytest.raises(ValidationError): UserResponse(**input_data)
    
def test_user_update_succecss():
    """tests that UserUpdate creates successfully with valid input"""
    input_data = {"first_name": "peregrin",
                  "last_name":"took",
                  "password" : "newPassword"}
    result = UserUpdate(**input_data)
    assert result.first_name == "peregrin"
    assert result.last_name == "took"
    assert result.password == "newPassword"
    
def test_user_update_empty():
    """test that UserUpdate can be created given no input"""
    input_data = {}
    result = UserUpdate(**input_data)
    assert result.first_name == None
    assert result.last_name == None
    assert result.password == None
    
def test_user_update_partial():
    """test that UserUpdate can be created given partial input data"""
    input_data = {"first_name": "pippin",}
    result = UserUpdate(**input_data)
    assert result.first_name == "pippin"
    assert result.last_name == None
    assert result.password == None

def test_user_update_invalid_name():
    """test that UserUpdate generates a validation error if given an invalid input"""
    input_data = {"first_name": "",}
    with pytest.raises(ValidationError): UserUpdate(**input_data)

def test_customer_create():
    """tests that CustomerCreate generates successfully with valid input"""
    input_data = {"email":"pippin@shire.me",
                "first_name": "peregrin",
                "last_name":"took",
                "password": "SecondBreakfast"}
    result = CustomerCreate(**input_data)
    assert result.email == "pippin@shire.me"
    assert result.first_name == "peregrin"
    assert result.last_name == "took"
    assert result.password == "SecondBreakfast"

def test_staff_create():
    """tests that StaffCreate generates successfully with valid input"""
    input_data = {"email":"pippin@shire.me",
                "first_name": "peregrin",
                "last_name":"took",
                "password": "SecondBreakfast"}
    result = StaffCreate(**input_data)
    assert result.email == "pippin@shire.me"
    assert result.first_name == "peregrin"
    assert result.last_name == "took"
    assert result.password == "SecondBreakfast"
    
def test_customer_create_invalid_password():
    """test that CustomerCreate generates a validation error if given an invalid password input"""
    input_data = {"email":"pippin@shire.me",
                "first_name": "peregrin",
                "last_name":"took",
                "password": "Seco"}
    with pytest.raises(ValidationError): CustomerCreate(**input_data)
    
def test_staff_create_invalid_password():
    """test that StaffCreate generates a validation error if given an invalid password input"""
    input_data = {"email":"pippin@shire.me",
                "first_name": "peregrin",
                "last_name":"took",
                "password": "Seco"}
    with pytest.raises(ValidationError): StaffCreate(**input_data)