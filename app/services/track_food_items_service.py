from collections import Counter
from typing import List
from fastapi import HTTPException
from app.schemas.track_food_items_schema import TrackFoodResponse
from app.repositories.order_items_repo import load_all as load_order_items
from app.repositories.orders_repo import load_all as load_orders
from app.services.food_item_service import get_food_by_id
from app.repositories.track_food_items_repo_csv import save_all as save_food_items, load_all as load_food_items

def get_stats_on_food(restaurant_id: int) -> List[TrackFoodResponse]:
    """Finds how often food items are ordered from a restaurant"""
    orders = load_orders()
    order_items = load_order_items()
    track_items = load_food_items()
    
    restaurant_id_str = str(restaurant_id)
    items_in_orders = [o["order_id"] for o in orders if str(o.get("restaurant_id")) == restaurant_id_str]
    
    if not items_in_orders:
        raise HTTPException(status_code=404, detail=f"Restaurant ID {restaurant_id} not found")
    
    items_in_order_items = [item for item in order_items if item.get("order_id") in items_in_orders]
    
    food_counter = Counter()
    for item in items_in_order_items:
        food_counter[item["food_item_id"]] += int(item["quantity"])
    
    result = []
    for food_id, count in food_counter.items():
        food = get_food_by_id(int(food_id))  
        if not food:
            continue  
        food_name = food["food_name"]
        
        result.append(
            TrackFoodResponse(
            food_item_id=food_id,
            order_count=count,
            food_name=food_name
        )
    )
    
    result_dicts = [item.dict() for item in result]
    track_items.extend(result_dicts)
    save_food_items(track_items)

    return result
    