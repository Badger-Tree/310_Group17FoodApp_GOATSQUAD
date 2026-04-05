from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    """Base pydantic class for reviews"""
    restaurant_id: int
    review : str = Field(min_length=1)
    rating : int = Field(ge=0, le=5)
    
class ReviewCreate(ReviewBase):
    """Extension of base review to create an order"""
    pass

class ReviewResponse(ReviewBase):
    """Extension of base review class used to send information about a review when requested"""
    review_id: str = Field(min_length=1)
    customer_id: str