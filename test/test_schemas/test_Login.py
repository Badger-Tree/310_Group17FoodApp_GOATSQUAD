from pydantic import ValidationError
import pytest

from app.schemas.Login import LoginRequest

def test_LoginRequest_success():
    """Tests that LoginRequests instantiates with valid input"""
    input_data = {"email" : "gandalf.white@council.me",
                "password" : "Glamdring"
                }
    result = LoginRequest(**input_data)
    assert result.email == "gandalf.white@council.me"
    
def test_LoginRequest_missing_fields():
    """Tests that LoginRequest raises a validation error if input has a missing field""" 
    input_data = {"email" : "gandalf.white@council.me"
                }
    with pytest.raises(ValidationError):LoginRequest(**input_data)
    
def test_LoginRequest_invalid_email():
    """Tests that LoginRequest raises a validation error if input has an invalid email field"""
    input_data = {"email" : "gandalf.whiteatcouncil.me",
                "password" : "Glamdring"
                }
    with pytest.raises(ValidationError):LoginRequest(**input_data)
    
def test_LoginRequest_invalid_password():
    """Tests that LoginRequest raises a validation error if input has a missing field"""
    input_data = {"email" : "gandalf.whiteatcouncil.me",
                    "password" : 123
                    }
    with pytest.raises(ValidationError):LoginRequest(**input_data)