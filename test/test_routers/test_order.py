from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from app.schemas.Order import OrderResponse
from app.schemas.OrderItem import OrderItemResponse
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Role import UserRole
from app.schemas.User import UserResponse
from app.services.order_service import CartItemResponse, CartResponse
import pytest
from unittest.mock import patch
from app.routers.order import router
from datetime import datetime

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# @pytest.fixture
# def mock_order_responses():
#     items = [
#         OrderItemResponse(
#             order_item_id="item1",
#             order_id="order123",
#             food_item_id=1,
#             quantity=2,
#             price_per_item=10.0
#         ),
#         OrderItemResponse(
#             order_item_id="item2",
#             order_id="order123",
#             food_item_id=2,
#             quantity=1,
#             price_per_item=6.66)]

#     order = OrderResponse(
#         order_id="order123",
#         restaurant_id="1",
#         customer_id="cust001",
#         delivery_address_id="addr001",
#         delivery_address="123 Hobbiton Lane",
#         delivery_id=None,
#         created_date=datetime(2026, 3, 15, 12, 0, 0),
#         status=OrderStatus.PENDING,
#         total_amount=26.66,
#         items=items
#     )
#     return order

@pytest.fixture
def mock_cart():
    cart_items = [
        CartItemResponse(
            food_item_id=1,
            quantity=1,
            price_per_item=1.00
        ),
        CartItemResponse(
            food_item_id=2,
            quantity=2,
            price_per_item=1.00
        )
    ]

    return CartResponse(
        cart_id="1",
        customer_id="1",
        restaurant_id=1,
        delivery_address_id="1",
        cart_items=cart_items
    )
    
@pytest.fixture
def mock_empty_cart():
    cart_items = []

    return CartResponse(
        cart_id="1",
        customer_id="1",
        restaurant_id=1,
        delivery_address_id="1",
        cart_items=cart_items
    )

@pytest.fixture
def mock_load_orders():
    return [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": None,
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
    }]

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
    return UserResponse(id="1",
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
        role=UserRole.OWNER,
        created_date=datetime(2026, 2, 20, 12, 34, 56))
    
@pytest.fixture
def mock_orders():
    return [
    {
        "order_id": "order123",
        "restaurant_id": 1,
        "customer_id": "cust001",
        "delivery_address_id": "addr001",
        "delivery_address": "123 Hobbiton Lane",
        "delivery_id": None,
        "created_date": datetime(2026, 3, 15, 12, 0, 0),
        "status": "PENDING",
        "total_amount": 26.66
    }
]
      
def test_create_order_success(mock_customer_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items,mock_cart ):
    """Tests that create_order will route valid input to process_order_service and return expected json with a 201 code """
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                        with patch("app.services.order_service.process_payment_service", return_value = True):
                            with patch("app.services.order_service.get_cart_by_id", return_value = mock_cart):
                                with patch("app.services.order_service.notify_order_placed") as mock_notfiy:
                                    response = client.post("/orders/create_order/1",headers={"token":"123"})
                                    assert response.status_code == 201
                                    response_data = response.json()
                                    assert "order_id" in response_data
                                    assert "customer_id" in response_data
                                    assert "restaurant_id" in response_data
                                    assert "delivery_address_id" in response_data
                                    assert "status" in response_data
                                    assert "total_amount" in response_data
                                    assert "items" in response_data
                                    assert response_data["customer_id"] == "1"
                                    assert response_data["total_amount"] == 3.00
                                    assert response_data["status"] == "PENDING"
                                    mock_notfiy.assert_called_once()
                    
def test_create_order_empty_order(mock_customer_response, mock_load_orders,mock_load_order_items,mock_save_orders,mock_save_all_order_items,mock_empty_cart):
    """Tests that create_order will throw a 422 error if an order has no order items"""                
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                with patch("app.services.order_service.save_all_orders", return_value = mock_save_orders):
                    with patch("app.services.order_service.save_all_order_items", return_value = mock_save_all_order_items):
                        with patch("app.services.order_service.process_payment_service", return_value = True):
                            with patch("app.services.order_service.get_cart_by_id", return_value = mock_empty_cart):
                                with patch("app.services.order_service.notify_order_placed") as mock_notfiy:
                                    response = client.post("/orders/create_order/1",headers={"token":"123"})
                                    assert response.status_code == 400
                                    mock_notfiy.assert_not_called()
                                                                        
def test_create_order_not_authorized(mock_staff_response):
    """Tests that create_order will throw a 403 error if the user does not have CUSTOMER role"""                
    with patch("app.routers.order.get_user_from_session", return_value = mock_staff_response):
            response = client.post("/orders/create_order/1",headers={"token":"123"})
            assert response.status_code == 403

def test_create_order_no_token():
    """Tests that create_order will throw a 422 error if the header has no token"""                
    response = client.post("/orders/create_order/1")
    assert response.status_code == 422
          
def test_get_order_by_id_succecss(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_id retrns an order response and 200 message if given valid data"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_id/order123")
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
                assert response_data["status"] == "PENDING"

def test_get_order_by_id_not_found(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_id returns a 404 error if service cannot locate given order order"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_id/notfound", )
                assert response.status_code == 404
                
def test_get_order_by_restaurant_id_success(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_restaurant_id returns an order response and 200 message if given valid data"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_restaurant/789")
                assert response.status_code == 200
                response_data = response.json()
                assert isinstance(response_data, list)
                assert len(response_data) == 1
                assert response_data[0]["restaurant_id"] == 789
                assert response_data[0]["order_id"] == "order123"
                
def test_get_order_by_restaurant_id_no_orders(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_restaurant_id returns an empty list and 200 message if given valid data that does not match results"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_restaurant/000")
                assert response.status_code == 200
                response_data = response.json()
                assert isinstance(response_data, list)
                assert len(response_data) == 0

def test_get_order_userid_success(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_userid returns an order response and 200 message if given valid data"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_user/cust456")
                assert response.status_code == 200
                response_data = response.json()
                assert isinstance(response_data, list)
                assert len(response_data) == 1
                assert response_data[0]["restaurant_id"] == 789
                assert response_data[0]["order_id"] == "order123"
                
def test_get_order_by_userid_no_orders(mock_customer_response, mock_load_orders,mock_load_order_items):
    """tests that get_order_by_userid returns an empty list and 200 message if given valid data that does not match results"""
    with patch("app.routers.order.get_user_from_session", return_value = mock_customer_response):
        with patch("app.services.order_service.load_orders", return_value = mock_load_orders):
            with patch("app.services.order_service.load_order_items", return_value = mock_load_order_items):
                response = client.get("/orders/get_order_by_user/nocust")
                assert response.status_code == 200
                response_data = response.json()
                assert isinstance(response_data, list)
                assert len(response_data) == 0
   
def test_get_order_status_by_id_success


# @router.get("/order_status", response_model = Enum, status_code=status.HTTP_200_OK)
# def get_order_status_by_id(orderid:str):
#     """Returns an order status enum given an order id str
#     Input: order id (string)
#     Output: OrderStatus (PENDING,APPROVED,CANCELED,IN_PREPARATION,OUT_FOR_DELIVERY,COMPLETED)
#     """
#     return get_order_status_by_id_service(orderid)