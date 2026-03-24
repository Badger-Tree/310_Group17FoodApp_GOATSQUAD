from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch
from app.main import app
import app.routers.delivery_router as delivery_router


client = TestClient(app)

#ASSIGNING DELIVERIES: SUCCESS
def test_assign_delivery_success():
    mock_delivery = {
        "order_id": "order-1",
        "address_id": "address-1",
        "delivery_id": "delivery-1",
        "courier_id": "courier-1",
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_status": "ASSIGNED"
    }

    with patch("app.routers.delivery_router.assign_delivery_to_courier", return_value=mock_delivery):
        response = client.put("/deliveries/assign/delivery-1/courier-1")

        assert response.status_code == 200
        assert response.json() == mock_delivery

#ASIGNING DELIVERIES: NO DELIVERY FOUND
def test_assign_delivery_delivery_not_found():
    with patch("app.routers.delivery_router.assign_delivery_to_courier",
               side_effect=HTTPException(status_code=404, detail="Delivery not found")):
        
        response = client.put("/deliveries/assign/nonexistent-delivery/courier-1")

        assert response.status_code == 404
        assert response.json() == {"detail": "Delivery not found"}

#UPDATING DELIVERIES: SUCCESS
def test_update_delivery_status_success():
    mock_delivery = {
        "order_id": "order-1",
        "address_id": "address-1",
        "delivery_id": "delivery-1",
        "courier_id": "courier-1",
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_status": "COMPLETED"
    }

    with patch("app.routers.delivery_router.update_delivery_status", return_value=mock_delivery):
        response = client.put("/deliveries/status/delivery-1/COMPLETED")

        assert response.status_code == 200
        assert response.json() == mock_delivery

#CANCELING DELIVERIES: SUCCESS
def test_cancel_delivery_success():
    mock_delivery = {
        "order_id": "order-1",
        "address_id": "address-1",
        "delivery_id": "delivery-1",
        "courier_id": None,
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_status": "CANCELED"
    }

    with patch("app.routers.delivery_router.cancel_delivery", return_value=mock_delivery):
        response = client.put("/deliveries/cancel/delivery-1")

        assert response.status_code == 200
        assert response.json() == mock_delivery