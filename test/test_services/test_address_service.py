from datetime import datetime
import pytest
from fastapi import HTTPException
from app.schemas.Address import AddressCreate, AddressUpdate
from app.services.address_service import get_address_by_id_service, get_address_by_customer_id_service, create_address_service, update_address_service, delete_address_service

def test_get_address_by_id_service_success(monkeypatch):
    """tests if get_address_by_id_service() gets address given valid input"""
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        }]
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    result = get_address_by_id_service("1")
    assert result.user_id == "456"
    assert result.street == "111 Shire Lane"
    assert result.city == "Hobbiton"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at driveway"
    assert result.created_date == datetime.fromisoformat("2025-01-20T11:34:56")
    
def test_get_address_by_id_service_id_not_found(monkeypatch):
    """tests if get_address_by_id_service() raises exception if addressid not found"""
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        }]
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    with pytest.raises(HTTPException, match = "Address '66' not found") as testException: get_address_by_id_service("66")
    assert testException.value.status_code ==404

def test_get_address_by_customer_id_service_success(monkeypatch):
    """tests if get_address_by_customer_id_service() gets address given valid customer id input"""
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    
    result = get_address_by_customer_id_service("456")
    assert len(result) == 2 
    assert result[0].address_id == "1"
    assert result[0].user_id == "456"
    assert result[0].street == "111 Shire Lane"
    assert result[0].city == "Hobbiton"
    assert result[0].postal_code == "H0B 1T5"
    assert result[0].instructions == "leave at driveway"
    assert result[0].created_date == datetime.fromisoformat("2025-01-20T11:34:56")
    
    assert result[1].address_id == "2"
    assert result[1].user_id == "456"
    assert result[1].street == "123 Westfalds Road"
    assert result[1].city == "Gondor"
    assert result[1].postal_code == "G0N D0R"
    assert result[1].instructions == "leave at driveway"
    assert result[1].created_date == datetime.fromisoformat("2024-01-20T11:34:56")
    

def test_get_address_by_customer_id_service_customer_not_found(monkeypatch):
    """tests if get_address_by_customer_id_service() raises exception if addressid not found"""
    
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        }]
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    with pytest.raises(HTTPException) as testException: get_address_by_customer_id_service("666")
    assert testException.value.status_code ==404

def test_create_address_service_success(monkeypatch):
    """tests if create_address_service() creates address given valid input"""
    
    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
        
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    def mock_uuid():
        return "test-user-id132"
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)
    monkeypatch.setattr("app.services.address_service.uuid.uuid4", mock_uuid)
    
    input_data = AddressCreate(
                street="123 Brandybuck Lane",
                city="Tuckburough",
                postal_code="H0B 1T5",
                instructions="leave at door"
    )
    result = create_address_service(input_data, "1")
    assert result.address_id == "test-user-id132"
    assert result.user_id == "1"
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at door"
    assert len(saved_data["addresses"]) == 3   
    
def test_create_address_service_partial_input(monkeypatch):
    """tests if create_address_service() creates address given valid input without optional fields"""

    def mock_load_users():
        return [{
        "id": "1",
        "email": "jane.doe@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "password",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }]
    
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
        
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    def mock_uuid():
        return "test-user-id132"
    monkeypatch.setattr("app.services.user_service.load_users", mock_load_users)
    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)
    monkeypatch.setattr("app.services.address_service.uuid.uuid4", mock_uuid)
    
    input_data = AddressCreate(
                street="123 Brandybuck Lane",
                city="Tuckburough",
                postal_code="H0B 1T5",
    )
    result = create_address_service(input_data, "1")
    assert result.address_id == "test-user-id132"
    assert result.user_id == "1"
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == None
    assert len(saved_data["addresses"]) == 3   


def test_update_address_service_success(monkeypatch):
    """tests if update_address_service() creates address given valid input"""
    
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
        
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)

    
    input_data = AddressUpdate(
        street="123 Brandybuck Lane",
        city="Tuckburough",
        postal_code="H0B 1T5",
        instructions = "instr"
    )
    
    result = update_address_service("2", input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "instr"
    
def test_update_address_service_partial_input(monkeypatch):
    """tests if update_address_service() updates address given valid input without optional fields"""
    
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
        
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)

    input_data = AddressUpdate(
        street="123 Brandybuck Lane",
        city="Tuckburough",
        postal_code="H0B 1T5",
    )
    
    result = update_address_service("2", input_data)
    assert result.street == "123 Brandybuck Lane"
    assert result.city == "Tuckburough"
    assert result.postal_code == "H0B 1T5"
    assert result.instructions == "leave at driveway"

def test_update_address_service_address_not_found(monkeypatch):
    """tests if update_address_service() raises excpetion if given invalid address id input"""

    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
        
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)

    input_data = AddressUpdate(
        street="123 Brandybuck Lane",
        city="Tuckburough",
        postal_code="H0B 1T5",
    )
    with pytest.raises(HTTPException) as testException: update_address_service("666", input_data)
    assert testException.value.status_code ==404

def test_delete_address_service_success(monkeypatch):
    """tests if delete_address_service() creates address given valid input"""
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
    
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)

    delete_address_service("1")
    
    assert len(saved_data["addresses"]) == 1
    assert saved_data["addresses"][0]["address_id"] == "2"
    
def test_delete_address_service_address_not_found(monkeypatch):
    """tests if delete_address_service() raises excpetion if given invalid address id input"""
    def mock_load_addresses():
        return [{
        "address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        },
        {"address_id": "2",
        "user_id": "456",
        "street": "123 Westfalds Road",
        "city": "Gondor",
        "postal_code": "G0N D0R",
        "instructions": "leave at driveway",
        "created_date": "2024-01-20T11:34:56"
        }]
    
    saved_data = {}
    def mock_save_addresses(addr):
        saved_data["addresses"] = addr
        return saved_data

    monkeypatch.setattr("app.services.address_service.load_addresses", mock_load_addresses)
    monkeypatch.setattr("app.services.address_service.save_addresses", mock_save_addresses)

    with pytest.raises(HTTPException) as testException: delete_address_service("777")
    assert testException.value.status_code ==404


    