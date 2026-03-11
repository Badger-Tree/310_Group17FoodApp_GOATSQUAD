
from fastapi import HTTPException
import pytest
from app.schemas.Role import UserRole
from app.services.authorization_service import has_role_service, require_role_service


def test_has_role_servicesuccess(mocker):
    """tests that has_role will successfully validate if a given user has a given role"""
    mock_user = mocker.Mock()
    
    mock_user.role = UserRole.CUSTOMER
    result = has_role_service(mock_user, UserRole.CUSTOMER)
    assert result == True  
    
    mock_user.role = UserRole.COURIER
    result = has_role_service(mock_user, UserRole.COURIER)
    assert result == True  
    
    
def test_has_role_servicesuccess(mocker):
    """tests that has_role will return false if a given user does not have a has a given role"""
    mock_user = mocker.Mock()
    mock_user.role = UserRole.CUSTOMER
    result = has_role_service(mock_user, UserRole.OWNER)
    assert result == False
    
    
def test_require_role_service_success(mocker):
    """tests that require_role_service returns None if user has required role"""
    mock_user = mocker.Mock()
    mock_user.role = UserRole.CUSTOMER
    
    result = require_role_service(mock_user, UserRole.CUSTOMER)
    assert result is None

def test_require_role_service_success(mocker):
    """tests that require_role_service raises an exception if user does not have required role"""
    mock_user = mocker.Mock()
    mock_user.role = UserRole.CUSTOMER
    
    with pytest.raises(HTTPException) as testException: require_role_service(mock_user, UserRole.OWNER)
    assert testException.value.status_code ==403
    
    