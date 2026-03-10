from datetime import datetime
from pydantic import BaseModel, ValidationError
from app.schemas.Role import UserRole
import pytest

from app.schemas.Token import Token, TokenResponse

def test_Token_success(): 
    """Tests that Token instantiates with valid input"""
    input_data = {"token": "gandalf"}
    result = Token(**input_data)
    assert result.token == "gandalf"
             
def test_Token_missing_data():
    """Tests that Token raises a validation error if input has a missing field""" 
    input_data = {}
    with pytest.raises(ValidationError):Token(**input_data)
    
def test_Token_invalid_data(): 
    """Tests that Token raises a validation error if input has an invalid field""" 
    input_data = {"token":123}
    with pytest.raises(ValidationError):Token(**input_data)
    
def test_TokenResponse_success(): 
    """Tests that TokenResponse instantiates with valid input"""
    input_data = {"token":"123",
                "user_id": "gandalf",
                "role" : "CUSTOMER",
                "created" : "2024-02-20T12:34:56",
                "expires" : "2024-03-20T12:34:56"}
    result = TokenResponse(**input_data)
    assert result.token == "123"
    assert result.user_id == "gandalf"
    assert result.role == UserRole.CUSTOMER
    assert result.created == datetime.fromisoformat("2024-02-20T12:34:56")
    assert result.expires == datetime.fromisoformat("2024-03-20T12:34:56")
    
def test_TokenResponse_missing_data(): 
    """Tests that TokenResponse raises a validation error if input has a missing field""" 
    input_data = {"token":"123",
                "role" : "CUSTOMER",
                "created" : "2024-02-20T12:34:56",
                "expires" : "2024-03-20T12:34:56"}
    with pytest.raises(ValidationError): TokenResponse(**input_data)
    
def test_TokenResponse_invalid_data(): 
    """Tests that TokenResponse raises a validation error if input has an invalid field""" 
    input_data = {"token":1234,
                "user_id": "gandalf",
                "role" : "CUSTOMER",
                "created" : "2024-02-20T12:34:56",
                "expires" : "2024-03-20T12:34:56"}
    with pytest.raises(ValidationError): TokenResponse(**input_data)