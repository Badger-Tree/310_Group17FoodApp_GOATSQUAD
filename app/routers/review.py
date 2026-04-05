from fastapi import APIRouter, HTTPException, Header, status
from app.schemas.Token import Token
from app.services.review_service import create_review_service
from app.schemas.Review import ReviewCreate, ReviewResponse
from app.services.session_manager_service import get_user_from_session

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/create_review/", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, token: str = Header(...)):
    """intakes a ReviewCreatePayload and sends to create_review_service"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    current_user_id = current_user.id
    create_review_service(current_user_id, payload)