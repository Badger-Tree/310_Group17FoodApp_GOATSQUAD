
from fastapi import HTTPException
from app.repositories.users_repo_csv import load_all as load_users
from app.schemas.Login import LoginRequest
from app.schemas.Token import Token, TokenResponse
from app.services.session_manager_service import create_session_service, expire_session_service
from app.repositories.users_repo_csv import load_all as load_users

def login_service(credentials: LoginRequest) -> TokenResponse:
    """Lets a user log in to the system. Input: LoginRequest(email, password). 
    Output: TokenResponse (userid, token, created, expires)"""
    if validate_credentials(credentials.email, credentials.password):
        token = create_session_service(credentials)
        return token
    raise HTTPException(status_code=401, detail=f"Incorrect credentials")

def logout_service(token: Token):
    """Lets a user log out of the system. Input: Token. Output: dict"""
    expire_session_service(token.token)
    return {"detail" : "logout successful"}
    
def validate_credentials(email : str, password : str) -> bool:
    """Validates a user's email and password. Input: email (str), password (str). Output: boolean"""
    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == password:
                return True
    return False