from fastapi import APIRouter, HTTPException, Header, status
from app.services.review_service import create_review_service
from app.schemas.Review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/create_review/", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, token: str = Header(...)):
    """intakes a ReviewCreatePayload and sends to create_review_service"""
    
    
    create_review_service()