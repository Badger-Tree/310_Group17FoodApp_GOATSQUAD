from fastapi import HTTPException
import pytest
from app.schemas.Review import ReviewCreate
from app.services.review_service import did_customer_order, get_review_service,has_customer_reviewed,create_review_service

mock_orders= [{
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
mock_reviews = [{
                "review_id": "review123",
                "customer_id": "cust456",
                "restaurant_id": 789,
                "review": "ok food",
                "rating": 4
                }]
mock_input = {
                "restaurant_id": 444,
                "review": "good food",
                "rating": 3
            }

mock_input = ReviewCreate(**mock_input)

def mock_save(input):
    return input

def test_did_customer_order_success(mocker):
    """tests that did_customer_order will return true if given valid input"""
    mocker.patch("app.services.review_service.get_orders_by_userid_service", return_value = mock_orders)

    result = did_customer_order("cust456", 789)
    assert result == True

def test_did_customer_order_customer_hasnt_ordered(mocker):
    """tests that did_customer_order will return false if the customer has no orders with provided restaurant id"""
    mocker.patch("app.services.review_service.get_orders_by_userid_service", return_value = mock_orders)
    
    result = did_customer_order("cust456", 111)
    assert result == False

def test_has_customer_reviewed_success(mocker):
    """tests that has_customer_reviewed will return true if given valid input"""
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    mocker.patch("app.services.review_service.save_reviews", return_value = [])
    
    result = has_customer_reviewed("cust456", 789)
    assert result == True

def test_has_customer_reviewed_customer_hasnt_ordered(mocker):
    """tests that has_customer_reviewed will return false if the customer has no orders with provided restaurant id"""
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    mocker.patch("app.services.review_service.save_reviews", return_value = [])
    
    result = has_customer_reviewed("cust456", 111)
    assert result == False
    
def test_create_review_service_success(mocker):
    """tests that create_review_service will save a review if given valid input"""
    mocker.patch("app.services.review_service.did_customer_order", return_value = True)
    mocker.patch("app.services.review_service.has_customer_reviewed", return_value = False)
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    mocker.patch("app.services.review_service.save_reviews", return_value = mock_save)

    result = create_review_service("cust456", mock_input)
    assert type(result.review_id) == str
    assert result.customer_id == "cust456"
    assert result.restaurant_id == 444
    assert result.review == "good food"
    assert result.rating == 3

def test_create_review_service_customer_hasnt_ordered(mocker):
    """tests that create_review_service will return an error a review if did_customer_order returns false """
    mocker.patch("app.services.review_service.did_customer_order", return_value = False)
    mocker.patch("app.services.review_service.has_customer_reviewed", return_value = False)
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    mocker.patch("app.services.review_service.save_reviews", return_value = mock_save)

    with pytest.raises(HTTPException) as testException: create_review_service("cust456", mock_input)
    assert testException.value.status_code ==422
    
def test_create_review_service_customer_already_reviewed(mocker):
    """tests that create_review_service will return an error a review if did_customer_order returns false """
    mocker.patch("app.services.review_service.did_customer_order", return_value = True)
    mocker.patch("app.services.review_service.has_customer_reviewed", return_value = True)
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    mocker.patch("app.services.review_service.save_reviews", return_value = mock_save)

    with pytest.raises(HTTPException) as testException: create_review_service("cust456", mock_input)
    assert testException.value.status_code ==422

def test_get_review_service_success(mocker):
    """tests that get_review_service will return a ReviewResponse given a matching review_id"""
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    
    result = get_review_service("review123")
    assert result.review_id == "review123"
    assert result.customer_id == "cust456"
    assert result.restaurant_id == 789
    assert result.review == "ok food"
    assert result.rating == 4
    
def test_get_review_service_invalid_input(mocker):
    """tests that get_review_service will return an exception if provided review_id is not found"""
    mocker.patch("app.services.review_service.load_reviews", return_value = mock_reviews)
    
    with pytest.raises(HTTPException) as testException: get_review_service("idnotfound")
    assert testException.value.status_code ==404
