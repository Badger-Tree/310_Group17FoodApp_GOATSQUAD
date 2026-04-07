from fastapi import APIRouter, Header
from app.schemas.track_items_schema import TrackRestaurantResponse
from app.services.track_items_service import get_stats_on_restaurants
from fastapi import HTTPException
from typing import List

router = APIRouter(prefix="/stat", tags=["stats"])

@router.get("/restaurant/stats", response_model=List[TrackRestaurantResponse], status_code=200)
def get_stats_for_restaurants():
    """Gets the stats of how often a restuarant recieves an order"""
    stats = get_stats_on_restaurants()  
    if not stats:
        raise HTTPException(status_code=404, detail="Error, no restaurant stats available")
    return stats


