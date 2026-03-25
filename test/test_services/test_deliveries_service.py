from unittest.mock import patch
from app.schemas.OrderStatus import OrderStatus
import pytest
from fastapi import HTTPException
from app.services.Delivery_service import (
    assign_delivery_to_courier,
    complete_delivery,
    create_delivery_service,
    pickup_delivery
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
                    "assignment": "COURIER"
            }
      ]

      with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.Delivery_service.load_orders", return_value = orders), \
            patch("app.services.Delivery_service.load_staff_assignments", return_value = staff_assignments), \
            patch("app.services.Delivery_service.save_all") as mock_save:

            result = assign_delivery_to_courier("delivery-1", "courier-1")

            assert result.delivery_id == "delivery-1"
            assert result.courier_id == "courier-1"
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



#PICK UP DELIVERIES: SUCCESS
def test_pick_up_delivery_success():
      deliveries = [
            {
                  "order_id": "order-1",
                  "courier_id": "courier-1",
                  "created_date": "2024-06-01T12:00:00Z",
                  "address_id": "address-1",
                  "delivery_id": "delivery-1"
            }
      ]

      mock_order_response = {
            "order_id": "order-1",
            "status": "OUT_FOR_DELIVERY",
      }

      with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.order_service.set_order_status_service", return_value = mock_order_response) as mock_set_status:

            result = pickup_delivery("delivery-1")
            
            assert result == mock_order_response
            mock_set_status.assert_called_once_with("order-1", OrderStatus.OUT_FOR_DELIVERY)
    
#PICK UP DELIVERIES: FAILURE DELIVERY NOT FOUND
def test_pick_up_delivery_not_found():
      with patch("app.services.Delivery_service.load_all", return_value = []), \
            patch("app.services.order_service.set_order_status_service") as mock_set_status:

            with pytest.raises(HTTPException) as exc_info:
                  pickup_delivery("delivery-1")

            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == "Delivery not found"
            mock_set_status.assert_not_called()

#COMPLETE DELIVERIES: SUCCESS
def test_complete_delivery_success():
      deliveries = [
            {
                  "order_id": "order-1",
                  "courier_id": "courier-1",
                  "created_date": "2024-06-01T12:00:00Z",
                  "address_id": "address-1",
                  "delivery_id": "delivery-1"
            }
      ]

      mock_order_response = {
            "order_id": "order-1",
            "status": "COMPLETED",
      }

      with patch("app.services.Delivery_service.load_all", return_value = deliveries), \
            patch("app.services.order_service.set_order_status_service", return_value = mock_order_response) as mock_set_status:

            result = complete_delivery("delivery-1")
            
            assert result == mock_order_response
            mock_set_status.assert_called_once_with("order-1", OrderStatus.COMPLETED)
    
#COMPLETE DELIVERIES: FAILURE DELIVERY NOT FOUND
def test_complete_delivery_not_found():
      with patch("app.services.Delivery_service.load_all", return_value = []), \
            patch("app.services.order_service.set_order_status_service") as mock_set_status:

            with pytest.raises(HTTPException) as exc_info:
                  complete_delivery("delivery-1")

            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == "Delivery not found"
            mock_set_status.assert_not_called()
