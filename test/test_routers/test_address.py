from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.routers.address import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

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
    
def mock_save_addresses(*args, **kwargs):
    return None

mock_address_response = {"address_id": "1",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"}

mock_address_list_response = [{
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


mock_address_create = {
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway"}

def test_get_address_by_id_success(mocker):
    """tests that get_address_by_id returns 200 status and address response json given valid data"""
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
        response = client.get("/addresses/by-id/1")
        assert response.status_code == 200
        assert response.json() == mock_address_response

def test_get_address_by_id_not_found(mocker):
    """tests that get_address_by_id throws a 404 exception if the address is not found"""
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
            response = client.get("/addresses/by-id/notfound")
            assert response.status_code == 404
            
def test_get_address_by_id_not_found(mocker):
    """tests that get_address_by_id throws a 404 exception if given no address input"""
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
            response = client.get("/addresses/by-id/")
            assert response.status_code == 404
            
            
def test_get_address_by_customer_id_success(mocker):
    """tests that get_address_by_customer_id returns a 200 message and address list of response json given valid customer id input"""
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
        response = client.get("/addresses/by-customer/456")
        assert response.status_code == 200
        assert response.json() == mock_address_list_response

def test_get_address_by_customer_id_not_found(mocker):
    """tests that get_address_by_customer_id returns a 404 message if no addresses match id"""
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
        response = client.get("/addresses/by-customer/000")
        assert response.status_code == 404

def  test_create_address_success(mocker):
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
    payload = mock_address_create
    with patch("app.services.address_service.load_addresses", mock_load_addresses):
        with patch("app.services.address_service.save_addresses", mock_save_addresses):
            with patch("app.routers.address.get_user_from_session", return_value = MockUserResponse(**mock_user_response)):
                response = client.post("/addresses/new", json = payload,headers={"token":"123"})
                assert response.status_code == 201
    
    


# @router.post("", response_model=AddressResponse, status_code=201)
# def create_address(payload: AddressCreate):
#     """Creates and saves a new address associated with a customer account
#     Intake: AddressCreate as payload(street, city, postal_code, instructions,user_id)
#     Return: AddressResponse (street, city, postal_code, instructions,address_id,user_id, created_date)"""
#     return create_address_service(payload)