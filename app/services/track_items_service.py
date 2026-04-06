from app.repositories.orders_repo import load_all as load_orders
from app.repositories.track_items_repo_csv import load_all as load_restaurant_items 
from app.repositories.track_items_repo_csv import save_all as save_restaurant_items 
from app.repositories.restaurants_repo_csv import load_all as load_restaurant_name
"""from app.repositories.order_items_repo import load_all as load_order_items"""
from collections import Counter
from fastapi import HTTPException


def get_stats(data, key):
    if not data: 
        raise HTTPException(status_code=400, detail="No orders yet")
    
    idSet = [item[key] for item in data if key in item]
    
    restaurant_data = load_restaurant_name()
    counts = Counter(idSet)
    result = []

    for restaurant_id, count in counts.items():
        restaurant_name = None
        for r in restaurant_data:
            if r["restaurant_id"] == restaurant_id:
                restaurant_name = r["restaurant_name"]
                break

        if restaurant_name is None:
            raise HTTPException(status_code=400, detail=f"restaurant id {restaurant_id} does not exist")
        
        result.append({"restaurant_name": restaurant_name, "order_count": count})

    return result



def get_stats_on_restaurants():
    orders = load_orders()
    items = load_restaurant_items()
    restaurant_stats = get_stats(orders, "restaurant_id")
    
    for stat in restaurant_stats:
        for item in items:
            if item["restaurant_name"] == stat["restaurant_name"]:
                item["order_count"] = stat["order_count"]
    save_restaurant_items(items)

    return restaurant_stats


"""
def get_stats_on_items(restaurant_id=None): will be here 

"""