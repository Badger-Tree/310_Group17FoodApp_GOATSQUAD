from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import unittest.mock
from unittest.mock import patch
import pytest
from app.routers.review import router
from app.schemas.Review import ReviewCreate, ReviewResponse
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
            },{
                "order_id": "order123",
                "customer_id": "cust456",
                "restaurant_id": 444,
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
                "review": "ok food",
                "rating": 4
            }]
@pytest.fixture
def mock_review_response():
    return ReviewResponse(review_id= "review123",
                customer_id= "cust456",
                restaurant_id= 789,
                review= "ok food",
                rating= 4)
    
def test_create_review_success(mock_customer_response, mock_orders, mock_load_reviews):
    """tests that create_review router will successfully pass a ReviewCreate and customer_id to create_review_service given valid input and session"""
    with patch("app.routers.review.get_user_from_session", return_value=mock_customer_response), \
        patch("app.services.review_service.get_orders_by_userid_service", return_value=mock_orders), \
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            mock_input = ReviewCreate(restaurant_id= 444,
                                        review= "good food",
                                        rating= 3)
            response = client.post(
                        "/reviews/create_review/",
                        json=mock_input.dict(),
                        headers={"token": "cust456"}
                    )
            assert response.status_code == 201
            mock_save.assert_called_once()
            
def test_create_review_customer_hasnt_ordered(mock_customer_response, mock_orders, mock_load_reviews):
    """tests that create_review router will return an error message if a customer has not ordered from given restaurant"""
    with patch("app.routers.review.get_user_from_session", return_value=mock_customer_response), \
        patch("app.services.review_service.get_orders_by_userid_service", return_value=mock_orders), \
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            mock_input = ReviewCreate(restaurant_id=565,
                                        review= "good food",
                                        rating= 3
                                        )
            response = client.post(
                        "/reviews/create_review/",
                        json=mock_input.dict(),
                        headers={"token": "cust456"}
                        )
            assert response.status_code == 422
            mock_save.assert_not_called()
            
def test_create_review_customer_already_reviewed(mock_customer_response, mock_orders, mock_load_reviews):
    """tests that create_review router will return an error message if a customer has already reviewed a given restaurant"""
    with patch("app.routers.review.get_user_from_session", return_value=mock_customer_response), \
        patch("app.services.review_service.get_orders_by_userid_service", return_value=mock_orders), \
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            mock_input = ReviewCreate(restaurant_id=789,
                                        review= "good food",
                                        rating= 3
                                        )
            response = client.post(
                        "/reviews/create_review/",
                        json=mock_input.dict(),
                        headers={"token": "cust456"}
                        )
            assert response.status_code == 422
            mock_save.assert_not_called()

def test_get_review_success(mock_load_reviews):
    """tests that get_review will pass a get request to get_review_service and return a ReviewResponse given a valid review_id"""
    with patch("app.services.review_service.load_reviews", return_value=mock_load_reviews):
        response = client.get("/reviews/get_review/review123")
        assert response.status_code == 200
        assert response.json()["review_id"] == "review123"
        assert response.json()["customer_id"] == "cust456"
        assert response.json()["restaurant_id"] == 789
        assert response.json()["review"] == "ok food"
        assert response.json()["rating"] == 4
        
def test_get_review_not_found(mock_load_reviews):
    """tests that get_review will pass a get request to get_review_service and return a ReviewResponse given a valid review_id"""
    with patch("app.services.review_service.load_reviews", return_value=mock_load_reviews):
        response = client.get("/reviews/get_review/reviewnotfound")
        assert response.status_code == 404 

def test_get_review_by_restaurant_success(mock_load_reviews):
    """tests that get_review_by_restaurant will return a list of ReviewResponses
    given a restaurant_id with matching reviews"""
    with patch("app.services.review_service.load_reviews", return_value=mock_load_reviews):
        response = client.get("/reviews/get_review_by_restaurant/789")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["review_id"] == "review123"
        
def test_get_review_by_restaurant_not_found(mock_load_reviews):
    """tests that get_review_by_restaurant will return an exception if no reviews are found matching provided restaurant id"""
    with patch("app.services.review_service.load_reviews", return_value=mock_load_reviews):
        response = client.get("/reviews/get_review_by_restaurant/555")
        assert response.status_code == 404
        
def test_delete_review_success(mock_load_reviews,mock_customer_response,mock_review_response):
    """tests that delete_review will successfully route a delete request to delete_review_service given valid input"""
    with patch("app.routers.review.get_user_from_session", return_value=mock_customer_response), \
        patch("app.routers.review.get_review_service", return_value=mock_review_response),\
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            response = client.delete(
                        "/reviews/delete/review123",
                        headers={"token": "cust456"}
                        )
            assert response.status_code == 204
            mock_save.assert_called_once()
            
def test_delete_review_not_found(mock_load_reviews,mock_customer_response,mock_review_response):
    """tests that delete_review will return an exception if it cannot find the requested review to delete"""
    with patch("app.routers.review.get_user_from_session", return_value=mock_customer_response), \
        patch("app.routers.review.get_review_service", return_value=mock_review_response),\
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            response = client.delete(
                        "/reviews/delete/notfound",
                        headers={"token": "cust456"}
                        )
            assert response.status_code == 404
            mock_save.assert_not_called()
            
def test_delete_review_service_user_found(mock_load_reviews,mock_customer_response,mock_review_response):
    """tests that delete_review will raise an error if it cannot find the user in the sesion"""
    with patch("app.routers.review.get_user_from_session", side_effect=HTTPException(status_code=401)), \
        patch("app.routers.review.get_review_service", return_value=mock_review_response),\
        patch("app.services.review_service.load_reviews", return_value=mock_load_reviews), \
        patch("app.services.review_service.save_reviews") as mock_save:
            
            response = client.delete(
                        "/reviews/delete/notfound",
                        headers={"token": "cust456"}
                        )
            assert response.status_code == 401
            mock_save.assert_not_called()
            