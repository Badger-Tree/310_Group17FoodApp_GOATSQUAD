from fastapi import APIRouter, Header
from app.schemas.track_food_items_schema import TrackFoodResponse
from app.services.track_food_items_service import get_stats_on_food
from fastapi import HTTPException
from typing import List

router = APIRouter(prefix="/food_stat", tags=["food_stats"])

@router.get("/food_items/{restaurant_id}/stats", response_model=List[TrackFoodResponse], status_code=200)
def get_stats_for_food_items(restaurant_id: int):
    """Gets the stats on food items"""
    stats = get_stats_on_food(restaurant_id)  
    if not stats:
        raise HTTPException(status_code=404, detail="Error, no food stats available")
    return stats