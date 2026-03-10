from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Class for login. The is the information the system needs to login/authenticate a user."""
    email: EmailStr
    password: str