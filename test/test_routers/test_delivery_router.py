from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch
from app.main import app



client = TestClient(app)

#ASSIGNING DELIVERIES: SUCCESS
def test_assign_delivery_success():
    mock_delivery = {
        "order_id": "order-1",
        "address_id": "address-1",
        "delivery_id": "delivery-1",
        "courier_id": "courier-1",
        "created_date": "2024-06-01T12:00:00Z",
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

#PICK UP DELIVERY: SUCCESSFUL
def test_pickup_delivery_success():
    mock_order = {
        "order_id": "order-1",
        "customer_id": "customer-1",
        "restaurant_id": 1,
        "delivery_id": "delivery-1",
        "status": "OUT_FOR_DELIVERY",
        "total_amount": 25.00,
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_address_id": "address-1",
        "items": []
    }

    with patch("app.routers.delivery_router.pickup_delivery", return_value=mock_order):
        response = client.put("/deliveries/pickup/delivery-1")

        assert response.status_code == 200
        assert response.json() == mock_order

#PICK UP DELIVERY: FAILURE DELIVERY NOT FOUND
def test_pickup_delivery_not_found():
    with patch("app.routers.delivery_router.pickup_delivery", side_effect=HTTPException(status_code=404, detail="Delivery not found")):
        
        response = client.put("/deliveries/pickup/nonexistent-delivery")

        assert response.status_code == 404
        assert response.json() == {"detail": "Delivery not found"}

#COMPLETE DELIVERY: SUCCESSFUL
def test_complete_delivery_success():
    mock_order = {
        "order_id": "order-1",
        "customer_id": "customer-1",
        "restaurant_id": 1,
        "delivery_id": "delivery-1",
        "status": "COMPLETED",
        "total_amount": 25.00,
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_address_id": "address-1",
        "items": []
    }

    with patch("app.routers.delivery_router.complete_delivery", return_value=mock_order):
        response = client.put("/deliveries/complete/delivery-1")

        assert response.status_code == 200
        assert response.json() == mock_order

#COMPLETE DELIVERY: FAILURE DELIVERY NOT FOUND
def test_complete_delivery_not_found():
    with patch("app.routers.delivery_router.complete_delivery", side_effect=HTTPException(status_code=404, detail="Delivery not found")):
        
        response = client.put("/deliveries/complete/nonexistent-delivery")

        assert response.status_code == 404
        assert response.json() == {"detail": "Delivery not found"}
