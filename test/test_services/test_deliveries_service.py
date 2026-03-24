from unittest.mock import patch
import pytest
from pydantic import ValidationError
from fastapi import HTTPException
from app.services.Delivery_service import (
    assign_delivery_to_courier,
    update_delivery_status,
    cancel_delivery,
    create_delivery_service
)

#CREATING DELIVERIES: SUCCESS
def test_create_delivery_success():
    mock_order = {
        "order_id": "order-1",
        "customer_id": "customer-1",
        "restaurant_id": "restaurant-1",
        "cart_id": "cart-1",
        "delivery_id": None,
        "status": "PENDING",
        "total_amount": 25.00,
        "created_date": "2024-06-01T12:00:00Z",
        "delivery_address_id": "address-1",
    }

    existing_deliveries = []

    with patch("app.services.Delivery_service.load_all", return_value=existing_deliveries), \
            patch("app.services.Delivery_service.save_all") as mock_save:
        
            result = create_delivery_service(mock_order)
    
    assert result.order_id == "order-1"
    assert result.address_id == "address-1"
    assert result.courier_id is None
    assert result.delivery_status == "PENDING"
    assert result.delivery_id is not None
    mock_save.assert_called_once()

#CREATING DELIVERIES: FAILURE (MISSING ADDRESS ID)
def test_create_delivery_missing_address_id():
      mock_order = {
        "order_id": "order-1",
        "customer_id": "customer-1",
        "restaurant_id": "restaurant-1",
        "cart_id": "cart-1",
        "delivery_id": None,
        "status": "PENDING",
        "total_amount": 25.00,
        "created_date": "2024-06-01T12:00:00Z",
      }

      with patch("app.services.Delivery_service.load_all", return_value=[]), \
            patch("app.services.Delivery_service.save_all") as mock_save:

            with pytest.raises(KeyError):
                create_delivery_service(mock_order)
            

            mock_save.assert_not_called()

#ASSIGNING DELIVERIES: SUCCESS
def test_assign_delivery_to_courier_success():
      deliveries = [
            {
                  "order_id": "order-1",
                  "courier_id": None,
                  "created_date": "2024-06-01T12:00:00Z",
                  "address_id": "address-1",
                  "delivery_status": "PENDING",
                  "delivery_id": "delivery-1"
            }
      ]

      orders = [
            {
                    "order_id": "order-1",
                    "customer_id": "customer-1",
                    "restaurant_id": "restaurant-1",
                    "cart_id": "cart-1",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 25.00,
                    "created_date": "2024-06-01T12:00:00Z",
                    "delivery_address_id": "address-1",
            }
      ]

      staff_assignments = [
            {
                    "assignment_id": "1",
                    "user_id": "courier-1",
                    "restaurant_id": "restaurant-1",
                    "role": "COURIER"
            }
      ]

      with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.Delivery_service.load_orders", return_value = orders), \
            patch("app.services.Delivery_service.load_staff_assignments", return_value = staff_assignments), \
            patch("app.services.Delivery_service.save_all") as mock_save:

            result = assign_delivery_to_courier("delivery-1", "courier-1")

            assert result.delivery_id == "delivery-1"
            assert result.courier_id == "courier-1"
            assert result.delivery_status == "ASSIGNED"
            mock_save.assert_called_once()

#ASSIGNING DELIVERIES: FAILURE DELIVERY NOT FOUND
def test_assign_delivery_to_courier_delivery_not_found():
    
    deliveries = []
    orders = []
    staff_assignments = []

    with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.Delivery_service.load_orders", return_value = orders), \
            patch("app.services.Delivery_service.load_staff_assignments", return_value = staff_assignments), \
            patch("app.services.Delivery_service.save_all") as mock_save:
          
            with pytest.raises(HTTPException) as exc_info:
                  assign_delivery_to_courier("delivery-1", "courier-1")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Delivery not found"
    mock_save.assert_not_called()

#ASSIGNING DELIVERIES: FAILURE INVALID COURIER
def test_assign_delivery_to_courier_invalid_courier():
      
      deliveries = [
            {
                  "order_id": "order-1",
                  "courier_id": None,
                  "created_date": "2024-06-01T12:00:00Z",
                  "address_id": "address-1",
                  "delivery_status": "PENDING",
                  "delivery_id": "delivery-1"
            }
      ]

      orders = [
            {
                  "order_id": "order-1",
                  "customer_id": "customer-1",
                  "restaurant_id": "restaurant-1",
                  "cart_id": "cart-1",
                  "delivery_id": None,
                  "status": "PENDING",
                  "total_amount": 25.00,
                  "created_date": "2024-06-01T12:00:00Z",
                  "delivery_address_id": "address-1",
            }
      ]

      staff_assignments = []

      with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.Delivery_service.load_orders", return_value = orders), \
            patch("app.services.Delivery_service.load_staff_assignments", return_value = staff_assignments), \
            patch("app.services.Delivery_service.save_all") as mock_save:

            with pytest.raises(HTTPException) as exc_info:
                  assign_delivery_to_courier("delivery-1", "courier-1")

            assert exc_info.value.status_code == 400
            assert exc_info.value.detail == "Invalid courier assignment"
            mock_save.assert_not_called()
    
#CANCEL DELIVERIES: SUCCESS
def test_cancel_delivery_success():
      
      deliveries = [
            {
                  "order_id": "order-1",
                  "courier_id": None,
                  "created_date": "2024-06-01T12:00:00Z",
                  "address_id": "address-1",
                  "delivery_status": "PENDING",
                  "delivery_id": "delivery-1"
            }
      ]

      with patch("app.services.Delivery_service.load_all", return_value= deliveries), \
            patch ("app.services.Delivery_service.save_all") as mock_save:

            result = cancel_delivery("delivery-1")
        
            assert result.delivery_id == "delivery-1"
            assert result.delivery_status == "CANCELED"
            mock_save.assert_called_once()