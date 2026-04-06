from pydantic import ValidationError
from datetime import datetime
import pytest
from app.schemas.Review import  ReviewCreate, ReviewBase, ReviewResponse

def test_ReviewBase_valid():
    """tests that ReviewBase is created successfully with valid input"""
    input_data = {"restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    
    result = ReviewBase(**input_data)
    assert result.restaurant_id == 3
    assert result.review == "ok food"
    assert result.rating == 5
    
def test_ReviewBase_invalid_input():
    """tests that ReviewBase raises an exception with invalid input in all fields"""
    input_data = {"restaurant_id" : "rest",
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
    input_data = {"restaurant_id" : 3,
                    "review" : 123,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
    input_data = {"restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : "five"}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
def test_ReviewBase_missing_input():
    """tests that ReviewBase raises an exception with missing input in all fields"""
    input_data = {
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
    input_data = {"restaurant_id" : 3,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
    input_data = {
                    "restaurant_id" : 3,
                    "review" : "ok food"}
    with pytest.raises(ValidationError): ReviewBase(**input_data)
    
def test_ReviewCreate_valid():
    """tests that ReviewCreate is created successfully with valid input"""
    input_data = {
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    
    result = ReviewCreate(**input_data)
    assert result.restaurant_id == 3
    assert result.review == "ok food"
    assert result.rating == 5
    
def test_ReviewCreate_invalid_input():
    """tests that ReviewCreate raises an exception with invalid input in all fields"""
    
    input_data = {
                    "restaurant_id" : "rest",
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
    input_data = {
                    "restaurant_id" : 3,
                    "review" : 123,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
    input_data = {
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : "rating"}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
def test_ReviewCreate_missing_input():
    """tests that ReviewCreate raises an exception with missing input in all fields"""
    input_data = {  
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
    input_data = {  "restaurant_id" : 3,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
    input_data = {  
                    "restaurant_id" : 3,
                    "review" : "ok food"}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
def test_ReviewCreate_invalid_rating():
    """tests that ReviewCreate raises an exception if rating is less than 0 or greater than 5"""
    input_data = {
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : -1}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)
    
    input_data = {
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 6}
    with pytest.raises(ValidationError): ReviewCreate(**input_data)

def test_ReviewResponse_valid():
    """tests that ReviewResponse is created successfully with valid input"""
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    
    result = ReviewResponse(**input_data)
    assert result.review_id == "1"
    assert result.customer_id == "2"
    assert result.restaurant_id == 3
    assert result.review == "ok food"
    assert result.rating == 5
    
def test_ReviewResponse_invalid_input():
    """tests that ReviewResponse raises an exception with missing input in all fields"""
    input_data = {"review_id" : 132,
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)

    input_data = {"review_id" : "1",
                    "customer_id" : 123,
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : "rest",
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : 456,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : "rating"}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
def test_ReviewResponse_missing_input():
    """tests that ReviewResponse raises an exception with missing input in all fields"""
    input_data = {"customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)

    input_data = {"review_id" : "1",
                    "restaurant_id" : 3,
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "review" : "ok food",
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "rating" : 5}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    
    input_data = {"review_id" : "1",
                    "customer_id" : "2",
                    "restaurant_id" : 3,
                    "review" : "ok food"}
    with pytest.raises(ValidationError): ReviewResponse(**input_data)
    