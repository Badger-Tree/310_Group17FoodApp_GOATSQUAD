from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from unittest.mock import patch

import pytest
from app.routers.order import router
from app.schemas.Review import ReviewCreate
from app.schemas.Role import UserRole
from app.schemas.User import UserResponse

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_customer_response():
    return UserResponse(id="cust456",
        email="pippin@example.com",
        first_name="peregrin",
        last_name="took",
        role=UserRole.CUSTOMER,
        created_date=datetime(2026, 2, 20, 12, 34, 56))
    
@pytest.fixture
def mock_orders():
        return[{
                "order_id": "order123",
                "customer_id": "cust456",
                "restaurant_id": 789,
                "cart_id": "cart101",
                "delivery_id": "delivery",
                "status": "PENDING",
                "total_amount": 26.66,
                "created_date": "2026-02-20T12:34:56",
                "delivery_address_id": "addr202"
            }]
@pytest.fixture
def mock_load_reviews():
        return [{
                "review_id": "review123",
                "customer_id": "cust456",
                "restaurant_id": 789,
                "review": 4,
                "rating": "ok food"
            }]
            
@pytest.fixture
def mock_input():
    input =  {
                "restaurant_id": 444,
                "review": "good food",
                "rating": 3
            }
    return ReviewCreate(**input)


def test_create_review(mock_customer_response, mock_orders, mock_load_reviews,mock_input):
    """tests that create_review router will successfully pass a ReviewCreate and customer_id to create_review_service given valid input and session"""
    patch("app.routers.order.get_user_from_session", return_value = mock_customer_response)
    patch("app.services.order_service.load_orders", return_value = mock_orders)
    patch("app.services.review_service.load_reviews", return_value = mock_load_reviews)
    patch("app.services.review_service.save_reviews")
        
    input = mock_input
    response = client.post("/reviews/create_review",headers={"token":"123"})
    
