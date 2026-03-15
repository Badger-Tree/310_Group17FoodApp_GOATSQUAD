from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.routers.address import router

app = FastAPI()
app.include_router(router)

app = FastAPI()

client = TestClient(app)

def test_get_address_by_id():
    mock_address =  {
        "address_id": "123",
        "user_id": "456",
        "street": "111 Shire Lane",
        "city": "Hobbiton",
        "postal_code": "H0B 1T5",
        "instructions": "leave at driveway",
        "created_date": "2025-01-20T11:34:56"
        }
    with patch("app.routers.address.get_address_by_id_service", return_value=mock_address) as mock_get_address_by_id_service:
        response = client.get("/addresses/by-id/123")
        assert response.status_code == 200
        assert response.json() == mock_address
        mock_get_address_by_id_service.called_once_with("123")