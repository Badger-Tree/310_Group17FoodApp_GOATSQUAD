from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from app.schemas.Address import AddressResponse
from app.schemas.Order import OrderResponse
from app.schemas.OrderItem import OrderItemResponse
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Role import UserRole
from app.schemas.User import UserResponse
from app.schemas.cart_item_schema import CartItemResponse
from app.schemas.notification import NotificationBase, NotificationStatus, NotificationType
from app.services.order_service import CartResponse, DeliveryResponse
import pytest
from unittest.mock import patch
from app.routers.order import router
from datetime import datetime

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_cart():
    return CartResponse(
        customer_id="cust456",
        cart_id="cart",
        cart_items=[
            CartItemResponse(
                cart_item_id="item_1",
                food_item_id=101,
                quantity=2,
                price_per_item=12.5,
                subtotal=25.0
            ),
            CartItemResponse(
                cart_item_id="item_2",
                food_item_id=202,
                quantity=1,
                price_per_item=8.75,
                subtotal=8.75
            ),
            CartItemResponse(
                cart_item_id="item_3",
                food_item_id=303,
                quantity=3,
                price_per_item=5.0,
                subtotal=15.0
            )
        ],
        total=48.75
    )
        
    
@pytest.fixture
def mock_empty_cart():
    return CartResponse(
        customer_id="cust456",
        cart_id="cart",
        cart_items=[],  # empty list
        total=0.0
    )

@pytest.fixture
def mock_load_orders():
    return [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        },{
        "order_id": "order456",
        "customer_id": "cust789",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "COMPLETED",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        },
        {
        "order_id": "order789",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "COMPLETED",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
        }
            ]

@pytest.fixture
def mock_save_orders(*args, **kwargs):
    return None

@pytest.fixture
def mock_load_order_items():
    return [{
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }]

@pytest.fixture
def mock_save_all_order_items(*args, **kwargs):
    return None

@pytest.fixture
def mock_customer_response():
    return UserResponse(id="cust456",
        email="pippin@example.com",
        first_name="peregrin",
        last_name="took",
        role=UserRole.CUSTOMER,
        created_date=datetime(2026, 2, 20, 12, 34, 56))
    
@pytest.fixture
def mock_staff_response():
    return UserResponse(id="2",
        email="pippin@example.com",
        first_name="peregrin",
        last_name="took",
        role=UserRole.STAFF,
        created_date=datetime(2026, 2, 20, 12, 34, 56))
      
@pytest.fixture
def mock_address_response():
    return AddressResponse(address_id= "4",
            user_id= "cust456",
            street= "111 Shire Lane",
            city= "Hobbiton",
            postal_code= "H0B 1T5",
            instructions= "leave at driveway",
            created_date = "2025-01-20T11:34:56")

@pytest.fixture
def mock_delivery_response():
    return DeliveryResponse(address_id= "4",
            order_id= "cust456",
            courier_id= "5",
            delivery_id = "newdelivery")
    
def test_create_order_success(mock_customer_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items,mock_cart,mock_address_response):
    """Tests that create_order will route valid input to process_order_service and return expected json with a 201 code """
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                        with patch("app.services.order_service.validate_item_inventory"):
                            with patch("app.services.order_service.process_payment_service", return_value = True):
                                with patch("app.services.order_service.get_cart_by_customer", return_value = mock_cart):
                                    with patch("app.services.order_service.get_food_by_id", return_value={"restaurant_id": 1}):
                                        with patch("app.services.order_service.notify_order_placed") as mock_order_notfiy:
                                            with patch("app.services.order_service.notify_payment_status") as mock_payment_notify:
                                                with patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response):
                                                    response = client.post("/orders/create_order/4",headers={"token":"123"})
                                                    assert response.status_code == 201
                                                    response_data = response.json()
                                                    assert "order_id" in response_data
                                                    assert "customer_id" in response_data
                                                    assert "restaurant_id" in response_data
                                                    assert "delivery_address_id" in response_data
                                                    assert "status" in response_data
                                                    assert "total_amount" in response_data
                                                    assert "items" in response_data
                                                    assert response_data["customer_id"] == "cust456"
                                                    assert response_data["total_amount"] == 48.75
                                                    assert response_data["status"] == "PENDING"
                                                    assert response_data["delivery_address_id"] == "4"
                                                    mock_payment_notify.assert_called_once()
                                                    mock_order_notfiy.assert_called_once()
                    
def test_create_order_empty_order(mock_customer_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items,mock_empty_cart):
    """Tests that create_order will throw a 422 error if an order has no order items"""                
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.validate_item_inventory"):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_payment_service", return_value = True):
                                with patch("app.services.order_service.get_cart_by_customer", return_value = mock_empty_cart):
                                    with patch("app.services.order_service.get_food_by_id", return_value={"restaurant_id": 1}):
                                        with patch("app.services.order_service.notify_order_placed") as mock_order_notfiy:
                                            with patch("app.services.order_service.notify_payment_status") as mock_payment_notify:
                                                with patch("app.services.order_service.get_address_by_id_service", return_value = mock_address_response):
                                                    response = client.post("/orders/create_order/4",headers={"token":"123"})
                                                    assert response.status_code == 400
                                                    mock_payment_notify.assert_not_called()
                                                    mock_order_notfiy.assert_not_called()  
                                                        
def test_create_order_not_authorized(mock_staff_response):
    """Tests that create_order will throw a 403 error if the user does not have CUSTOMER role"""                
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
            response = client.post("/orders/create_order/4",headers={"token":"123"})
            assert response.status_code == 403

def test_create_order_no_token():
    """Tests that create_order will throw a 422 error if the header has no token"""                
    response = client.post("/orders/create_order/4")
    assert response.status_code == 422
          
def test_get_order_by_id_succecss(mock_load_orders,mock_load_order_items):
    """tests that get_order_by_id retrns an order response and 200 message if given valid data"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/get_order_by_id/order123")
            assert response.status_code == 200
            response_data = response.json()
            assert "order_id" in response_data
            assert "customer_id" in response_data
            assert "restaurant_id" in response_data
            assert "delivery_address_id" in response_data
            assert "delivery_id" in response_data
            assert "status" in response_data
            assert "total_amount" in response_data
            assert "items" in response_data
            assert response_data["customer_id"] == "cust456"
            assert response_data["total_amount"] == 26.66
            assert response_data["status"] == "PENDING"
            
def test_get_order_by_restaurant_id_success(mock_load_orders,mock_load_order_items):
    """tests that get_order_by_restaurant_id returns an order response and 200 message if given valid data"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/get_order_by_restaurant/789")
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 3
            assert response_data[0]["restaurant_id"] == 789
            assert response_data[0]["order_id"] == "order123"
                
def test_get_order_by_restaurant_id_no_orders(mock_load_orders,mock_load_order_items):
    """tests that get_order_by_restaurant_id returns an empty list and 200 message if given valid data that does not match results"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/get_order_by_restaurant/000")
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 0

def test_get_order_userid_success(mock_load_orders,mock_load_order_items):
    """tests that get_order_by_userid returns an order response and 200 message if given valid data"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/get_order_by_user/cust456")
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 2
            assert response_data[0]["restaurant_id"] == 789
            assert response_data[0]["order_id"] == "order123"
                
def test_get_order_by_userid_no_orders(mock_load_orders,mock_load_order_items):
    """tests that get_order_by_userid returns an empty list and 200 message if given valid data that does not match results"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/get_order_by_user/nocust")
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 0
   
def test_get_order_status_by_id_success(mock_load_orders,mock_load_order_items):
    """tests that get_order_status_by_id will return a status enum given a valid order id"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/order_status/order123")
            assert response.status_code == 200
            response_data = response.json()
            assert response_data == "PENDING"
            
def test_get_order_status_by_id_order_not_found(mock_load_orders,mock_load_order_items):
    """tests that get_order_status_by_id will return a 404 response given an order status that does not match to an order"""
    with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
        with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
            response = client.get("/orders/order_status/123")
            assert response.status_code == 404
            response_data = response.json()
            assert response_data == {'detail': 'Order not found'} 

def test_cancel_order_customer_success(mock_customer_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """test that cancel_order_customer will return an OrderResponse and 200 message if given valid input"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                with patch("app.services.order_service.notify_refund_issued") as mock_payment_notfiy: 
                                    with patch("app.services.order_service.notify_order_status_update_customer_cancels") as mock_order_notfiy:
                                            response = client.put("/orders/cancel_order_customer/order123",headers={"token":"123"})
                                            assert response.status_code == 200
                                            response_data = response.json()
                                            assert response_data["status"] == "CANCELED"
    
def test_cancel_order_customer_not_authenticated():
    """tests that cancel_order_customer will return a 401 error if user is not authorized to cancel order"""
    with patch("app.routers.order.get_user_from_session", side_effect=HTTPException(status_code=401, detail="User not found")):
        response = client.put("/orders/cancel_order_customer/order123",headers={"token":"123"})
        assert response.status_code == 401
        
def test_cancel_order_customer_not_authorized(mock_staff_response):
    """tests that cancel_order_customer will return a 403 error if user does not have a staff role"""
    with patch("app.routers.order.get_user_from_session", return_value=mock_staff_response):
        response = client.put("/orders/cancel_order_customer/order123",headers={"token":"123"})
        assert response.status_code == 403
    
def test_cancel_order_customer_order_not_found(mock_customer_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """tests that cancel_order_customer will return a 404 error if order is not found"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                with patch("app.services.order_service.notify_refund_issued") as mock_payment_notfiy: 
                                    with patch("app.services.order_service.notify_order_status_update_customer_cancels") as mock_order_notfiy:
                                        response = client.put("/orders/cancel_order_customer/noorder",headers={"token":"123"})
                                        assert response.status_code == 404

def test_cancel_order_customer_order_accepted(mock_customer_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """tests that cancel_order_customer will return a 400 error if order is already accepted"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                        response = client.put("/orders/cancel_order_customer/order789",headers={"token":"123"})
                                        assert response.status_code == 400

    
def test_cancel_order_customer_wrong_customer(mock_customer_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """tests that cancel_order_customer will return a 403 error a customer tries to cancel an order that isn't theirs"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                        response = client.put("/orders/cancel_order_customer/order456",headers={"token":"123"})
                                        assert response.status_code == 403
def test_cancel_order_customer_not_authenticated():
    """tests that cancel_order_customer will return a 401 error if user is not authorized to cancel order"""
    with patch("app.routers.order.get_user_from_session", side_effect=HTTPException(status_code=401, detail="User not found")):
        response = client.put("/orders/cancel_order_restaurant/order123",headers={"token":"123"})
        assert response.status_code == 401
        
def test_cancel_order_restaurant_success(mock_staff_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """test that cancel_order_staff will return an OrderResponse and 200 message if given valid input"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                with patch("app.services.order_service.process_refund_service", return_value = True):
                                    with patch("app.services.order_service.notify_refund_issued") as mock_payment_notfiy: 
                                        with patch("app.services.order_service.notify_order_status_update") as mock_order_notfiy:
                                                response = client.put("/orders/cancel_order_restaurant/order123",headers={"token":"123"})
                                                assert response.status_code == 200
                                                response_data = response.json()
                                                assert response_data["status"] == "CANCELED"
    
def test_cancel_order_restaurant_not_authorized(mock_customer_response):
    """tests that cancel_order_restaurant will return a 403 error if user is not authorized to cancel order"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        response = client.put("/orders/cancel_order_restaurant/order123",headers={"token":"123"})
        assert response.status_code == 403
    
def test_cancel_order_restaurant_order_not_found(mock_staff_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """tests that cancel_order_restaurant will return a 404 error if order is not found"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                        response = client.put("/orders/cancel_order_restaurant/noorder",headers={"token":"123"})
                                        assert response.status_code == 404
  
def test_cancel_order_restaurant_order_accepted(mock_staff_response,mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items):
    """tests that cancel_order_restaurant will return a 400 error if order is already accepted"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
            with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
                with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                    with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                        with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                            with patch("app.services.order_service.process_refund_service", return_value = True):
                                        response = client.put("/orders/cancel_order_restaurant/order456",headers={"token":"123"})
                                        assert response.status_code == 400
    
def test_accept_order_success(mock_staff_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_delivery_response):
    """tests that accept_order will return an Order Response and 200 message if given valid input"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.notify_order_status_update") as mock_order_notfiy:
                        with patch("app.services.order_service.create_delivery_service", return_value = mock_delivery_response):
                            response = client.put("/orders/accept_order/order123",headers={"token":"123"})
                            assert response.status_code == 200
                            response_data = response.json()
                            assert "order_id" in response_data
                            assert "customer_id" in response_data
                            assert "restaurant_id" in response_data
                            assert "delivery_address_id" in response_data
                            assert "status" in response_data
                            assert "total_amount" in response_data
                            assert "items" in response_data
                            assert response_data["customer_id"] == "cust456"
                            assert response_data["total_amount"] == 26.66
                            assert response_data["status"] == "ACCEPTED"
                            assert response_data["delivery_id"] == "newdelivery"
                            mock_order_notfiy.assert_called_once()
                                                            
def test_accept_order_success_order_not_found(mock_staff_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_delivery_response):
    """tests that accept_order will return an 404 message if order is not found"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.notify_order_status_update") as mock_notfiy:
                            response = client.put("/orders/accept_order/noorder",headers={"token":"123"})
                            assert response.status_code == 404

def test_accept_order_not_authenticated():
    """tests that accept order will return a 401 message if user is not logged in"""
    with patch("app.routers.order.get_user_from_session", side_effect=HTTPException(status_code=401, detail="User not found")):
        response = client.put("/orders/accept_order/order123",headers={"token":"123"})
        assert response.status_code == 401
    
def test_accept_order_restaurant_not_authorized(mock_customer_response):
    """tests that accept order will return a 403 messages if the user is not authorized to use method"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        response = client.put("/orders/accept_order/order123",headers={"token":"123"})
        assert response.status_code == 403