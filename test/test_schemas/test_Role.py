from pydantic import ValidationError
from app.schemas.Role import UserRole
import pytest

def test_UserRole_success():
    """tests that Role is created successfulyl with valid input"""
    input_data = "CUSTOMER"
    result = UserRole(input_data)
    assert result == UserRole.CUSTOMER
    
    input_data = "OWNER"
    result = UserRole(input_data)
    assert result == UserRole.OWNER

def test_UserRole_invalid_input():
    """tests that UserRole will raise an exception if given invalid input"""
    input_data = "Owner"
    with pytest.raises(ValueError): UserRole(input_data)