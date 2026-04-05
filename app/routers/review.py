from typing import List

from fastapi import APIRouter, HTTPException, Header, status
from app.schemas.Token import Token
from app.services.review_service import create_review_service, get_review_by_restaurant_service, get_review_service,delete_review_service
from app.schemas.Review import ReviewCreate, ReviewResponse
from app.services.session_manager_service import get_user_from_session

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/create_review/", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, token: str = Header(...)):
    """intakes a ReviewCreatePayload and sends to create_review_service"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    return create_review_service(current_user_id, payload)

@router.get("/get_review/{review_id}",response_model=ReviewResponse,status_code=status.HTTP_200_OK)
def get_review(review_id:str):
    """passes request to get_review_service and returns a ReviewResponse"""
    return get_review_service(review_id)

@router.get("/get_review_by_restaurant/{restaurant_id}",response_model=List[ReviewResponse],status_code=status.HTTP_200_OK)
def get_review_by_restaurant(restaurant_id:int):
    """passes request to get_review_service and returns a list of ReviewResponse objects for one restaurant"""
    return get_review_by_restaurant_service(restaurant_id)

@router.delete("/delete/{review_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id:str, token: str = Header(...)):
    """checks if review is being deleted by the user who submits it and passes request to delete_review_service"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_review = get_review_service(review_id)
    if current_user.id != current_review.customer_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    delete_review_service(review_id)
    return