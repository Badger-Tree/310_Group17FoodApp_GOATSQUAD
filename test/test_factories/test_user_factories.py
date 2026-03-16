import uuid
from app.factories.user_factory import UserFactory
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, StaffCreate

mock_payload = CustomerCreate(
        email = "darcy@pemberly.uk",
        first_name = "Fitzwilliam",
        last_name="Darcy",
        password="georgiana"
    )

def test_create_base_user():
    """Tests that the base factory is successfully instantiating a CustomerCreate given a valid payload and Customer role""" 
    result = UserFactory.create_base_user(mock_payload, UserRole.CUSTOMER)
    assert result["email"] == "darcy@pemberly.uk"
    assert result["first_name"] == "Fitzwilliam"
    assert result["last_name"] == "Darcy"
    assert result["password"] == "georgiana"

    
def test_customer_factory_create_user():
    """Tests that the Customer factory class is successfully instantiating a CustomerCreate given a valid payload and Customer role"""
    result = UserFactory.create_base_user(mock_payload, UserRole.CUSTOMER)
    assert result["email"] == "darcy@pemberly.uk"
    assert result["first_name"] == "Fitzwilliam"
    assert result["last_name"] == "Darcy"
    assert result["password"] == "georgiana"
    assert result["role"] == UserRole.CUSTOMER
    assert isinstance(result["id"], str)
    uuid.UUID(result["id"])
    
    

def test_staff_factory_create_user():
    """Tests that the Staff factory class is successfully instantiating a StaffCreate given a valid payload and Staff role"""
    result = UserFactory.create_base_user(mock_payload, UserRole.STAFF)
    assert result["email"] == "darcy@pemberly.uk"
    assert result["first_name"] == "Fitzwilliam"
    assert result["last_name"] == "Darcy"
    assert result["password"] == "georgiana"
    assert result["role"] == UserRole.STAFF
    assert isinstance(result["id"], str)
    uuid.UUID(result["id"])
    
    