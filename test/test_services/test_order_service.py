from fastapi import HTTPException
import pytest
from app.services.order_service import cancel_order_customer_service


def test_cancel_order_customer_service_success(mocker):
    """tests that cancel_order_customer_service() will successfully cancel an order given valid order id from customer side"""
    mock_orders = [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    
    result = cancel_order_customer_service("order123")
    assert result.order_id == ("order123")
    
def test_cancel_order_customer_service_order_not_found(mocker):
    """tests that cancel_order_customer_service() will generate an error if order is not found by order id"""
    mock_orders = [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    with pytest.raises(HTTPException) as testException: cancel_order_customer_service("order6")
    assert testException.value.status_code ==404
        
def test_cancel_order_customer_service_order_approved(mocker):
    """tests that cancel_order_customer_service() will generate an error if order has already been approved"""
    mock_orders = [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": "rest789",
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "APPROVED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    with pytest.raises(HTTPException) as testException: cancel_order_customer_service("order123")
    assert testException.value.status_code ==400