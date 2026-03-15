from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.routers.address import router
import pytest

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_load_addresses():
    return[{
            "address_id": "1",
            "user_id": "456",
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway",
            "created_date": "2025-01-20T11:34:56"},
                        
            {"address_id": "2",
            "user_id": "456",
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway",
            "created_date": "2025-01-20T11:34:56"
            }]
@pytest.fixture
def mock_save_addresses(*args, **kwargs):
    return None

@pytest.fixture
def mock_address_response():
    return {"address_id": "1",
            "user_id": "456",
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway",
            "created_date": "2025-01-20T11:34:56"}
    
@pytest.fixture
def mock_address_list_response():
    return [{
            "address_id": "1",
            "user_id": "456",
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway",
            "created_date": "2025-01-20T11:34:56"},
                    
            {"address_id": "2",
            "user_id": "456",
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway",
            "created_date": "2025-01-20T11:34:56"
            }]
@pytest.fixture
def mock_address_create():
    return {
            "street": "111 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway"}
@pytest.fixture
def mock_address_update():
    return {
            "street": "222 Shire Lane",
            "city": "Hobbiton",
            "postal_code": "H0B 1T5",
            "instructions": "leave at driveway"}

def test_get_address_by_id_success(mock_load_addresses,mock_address_response):
    """tests that get_address_by_id returns 200 status and address response json given valid data"""
    with patch("app.services.address_service.load_addresses", return_value=mock_load_addresses):
        response = client.get("/addresses/by-id/1")
        assert response.status_code == 200
        assert response.json() == mock_address_response

def test_get_address_by_id_not_found(mock_load_addresses):
    """tests that get_address_by_id throws a 404 exception if the address is not found"""
    with patch("app.services.address_service.load_addresses", return_value=mock_load_addresses):
            response = client.get("/addresses/by-id/notfound")
            assert response.status_code == 404
            
def test_get_address_by_id_not_found(mock_load_addresses):
    """tests that get_address_by_id throws a 404 exception if given no address input"""
    with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
            response = client.get("/addresses/by-id/")
            assert response.status_code == 404
                        
def test_get_address_by_customer_id_success(mock_load_addresses, mock_address_list_response):
    """tests that get_address_by_customer_id returns a 200 message and address list of response json given valid customer id input"""
    with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
        response = client.get("/addresses/by-customer/456")
        assert response.status_code == 200
        assert response.json() == mock_address_list_response

def test_get_address_by_customer_id_not_found(mock_load_addresses):
    """tests that get_address_by_customer_id returns a 404 message if no addresses match id"""
    with patch("app.services.address_service.load_addresses", return_value=mock_load_addresses):
        response = client.get("/addresses/by-customer/000")
        assert response.status_code == 404

def  test_create_address_success(mock_load_addresses,mock_save_addresses, mock_address_create):
    """tests that get_address_by_id returns 200 status and address response json given valid data"""
    class MockUserResponse:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    mock_user_response = {
        "email": "pippin@example.com",
        "id": "1",
        "first_name": "peregrin",
        "last_name": "took",
        "role": "CUSTOMER",
        "created_date": "2026-02-20T12:34:56"
        }
    with patch("app.routers.address.validate_token_service", return_value = "123"):
        with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
            with patch("app.services.address_service.save_addresses", return_value = mock_save_addresses):
                with patch("app.routers.address.get_user_from_session", return_value = MockUserResponse(**mock_user_response)):
                    response = client.post("/addresses/new", json = mock_address_create,headers={"token":"123"})
                    assert response.status_code == 201

def  test_create_address_not_authenticated(mock_address_create):
    with patch("app.routers.address.get_user_from_session", side_effect=HTTPException(status_code=404, detail="User not found")):
                response = client.post("/addresses/new", json = mock_address_create,headers={"token":"123"})
                assert response.status_code == 404
    
def test_create_address_missing_token(mock_address_create):
    """Tests that create_address will throw an exception if there is no token in the header"""  
    response = client.post("/addresses/new", json = mock_address_create)
    assert response.status_code == 422

def test_update_address_missing_token(mock_load_addresses,mock_save_addresses):
    """Tests that update_address will throw an exception if there is no token in the header"""
    with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
        with patch("app.services.address_service.save_addresses",  return_value = mock_save_addresses):
                response = client.put("/addresses/update/2")
                assert response.status_code == 422
                
def test_update_address_not_authenticated(mock_address_update):
    with patch("app.routers.address.get_user_from_session", side_effect=HTTPException(status_code=404, detail="User not found")):
                response = client.put("/addresses/update/3", json = mock_address_update,headers={"token":"1"})
                assert response.status_code == 404

def test_update_address_success(mock_address_update,mock_address_response):
    """tests that update_address will return a 200 status and updated json given valid input"""
    with patch("app.routers.address.validate_token_service", return_value = "123"):
        with patch("app.routers.address.update_address_service", return_value = mock_address_response):                
                response = client.put("/addresses/update/2", json = mock_address_update,headers={"token":"123"} )
                assert response.status_code == 200
                
def test_update_address_partial_input(mock_address_response):
    """tests that update_address will return a 200 status and updated json given valid partial input"""
    payload = {"street": "222 Shire Lane"}
    with patch("app.routers.address.validate_token_service", return_value = "123"):
        with patch("app.routers.address.update_address_service", return_value = mock_address_response):                
                response = client.put("/addresses/update/2", json = payload,headers={"token":"123"} )
                assert response.status_code == 200
                assert response.json()== mock_address_response

def test_update_address_address_not_found(mock_load_addresses,mock_save_addresses):
    """tests that update_address will return a 404 status if the address to update is not found"""
    payload = {"street": "222 Shire Lane"}
    with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
        with patch("app.services.address_service.save_addresses", return_value = mock_save_addresses):
            response = client.put("/addresses/update/notfound", json = payload,headers={"token":"123"})
            assert response.status_code == 404
                
def test_delete_address_success(mock_load_addresses,mock_save_addresses):
    """tests that delete_address will return a 204 status if a delete was succsesful"""
    with patch("app.routers.address.validate_token_service", return_value = "123"):
        with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
            with patch("app.services.address_service.save_addresses", return_value = mock_save_addresses):        
                response = client.delete("/addresses/delete/2",headers={"token":"123"})
                assert response.status_code == 204
                            
def test_delete_address_not_found(mock_load_addresses,mock_save_addresses):
    """tests that will return a 404 status if the address to delete is not found"""
    with patch("app.routers.address.validate_token_service", return_value = "123"):
        with patch("app.services.address_service.load_addresses", return_value = mock_load_addresses):
            with patch("app.services.address_service.save_addresses", return_value = mock_save_addresses):
                response = client.delete("/addresses/delete/notfound",headers={"token":"123"})
                assert response.status_code == 404