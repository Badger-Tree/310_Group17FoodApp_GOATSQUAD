from typing import List

from fastapi import HTTPException
from app.repositories.reviews_repo import load_all as load_reviews, save_all as save_reviews
import uuid
from app.schemas.Review import ReviewCreate, ReviewResponse
from app.services.order_service import get_orders_by_userid_service

get_orders_by_userid_service

def did_customer_order(customer_id:str, restaurant_id: int) -> bool:
    """checks if customer has placed an order with the restaurant they are reviewing"""
    customer_orders = get_orders_by_userid_service(customer_id)
    for order in customer_orders:
        if order["restaurant_id"] == restaurant_id:
            return True
    return False
    
def has_customer_reviewed(customer_id, restaurant_id) -> bool:
    """checks if customer has already reviewed the restaurant they are reviewing"""
    reviews = load_reviews()
    for review in reviews:
        if review["customer_id"] == customer_id and review["restaurant_id"] == restaurant_id:
            return True
    return False
    
def create_review_service(customer_id: str,payload: ReviewCreate):
    """Intakes a CreateOrder object and sends it to the orders report"""
    if not did_customer_order(customer_id, payload.restaurant_id):
        raise HTTPException(status_code=422, detail=f"Customer has not ordered from restaurant") 

    if has_customer_reviewed(customer_id, payload.restaurant_id): 
        raise HTTPException(status_code=422, detail=f"Customer has already reviewed restaurant")
     
    reviews = load_reviews()
    review_id = str(uuid.uuid4())
    
    review = {"review_id": review_id,
                "customer_id": customer_id,
                "restaurant_id": payload.restaurant_id,
                "review": payload.review,
                "rating": payload.rating
            }
    reviews.append(review)
    save_reviews(reviews)
    return ReviewResponse(**review)

def get_review_service(review_id: str)-> ReviewResponse:
    """returns a ReviewResponse from csv if the review_id exists"""
    reviews = load_reviews()
    for review in reviews:
        if review_id == review["review_id"]:
            return ReviewResponse(**review)
    raise HTTPException(status_code=404, detail=f"review {review_id} not found")

def get_review_by_restaurant_service(restaurant_id: int) -> List[ReviewResponse]:
    """returns a list of ReviewResponses associated with provided restaurant or an exception if any exist"""
    reviews = load_reviews()
    restaurant_reviews = []
    for review in reviews:
        if restaurant_id == review["restaurant_id"]:
            restaurant_reviews.append(ReviewResponse(**review))
    if restaurant_reviews:
        return restaurant_reviews
    raise HTTPException(status_code=404, detail=f"no reviews found for restaurant {restaurant_id}")

def delete_review_service(review_id: str):
    reviews = load_reviews()
    found_review = False
    for index, review in enumerate(reviews):
        if review["review_id"] == review_id:
            reviews.pop(index)
            found_review = True
    if not found_review:
        raise HTTPException(status_code=404, detail=f"review {review_id} not found")
    save_reviews(reviews)
    return