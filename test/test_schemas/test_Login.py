from pydantic import ValidationError
import pytest

from app.schemas.Login import LoginRequest


def test_LoginRequest_success():
    input_data = {"email" : "gandalf.white@council.me",
                "password" : "Glamdring"
                }
    result = LoginRequest(**input_data)
    assert result.email == "gandalf.white@council.me"
    
def test_LoginRequest_missing_fields():
    input_data = {"email" : "gandalf.white@council.me"
                }
    with pytest.raises(ValidationError):LoginRequest(**input_data)
    
def test_LoginRequest_invalid_email():
    input_data = {"email" : "gandalf.whiteatcouncil.me",
                "password" : "Glamdring"
                }
    with pytest.raises(ValidationError):LoginRequest(**input_data)
    
def test_LoginRequest_invalid_password():
        input_data = {"email" : "gandalf.whiteatcouncil.me",
                    "password" : 123
                    }
        with pytest.raises(ValidationError):LoginRequest(**input_data)