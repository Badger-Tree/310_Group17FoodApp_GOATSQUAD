from app.repositories.orders_repo import load_all as load_orders
from app.repositories.track_items_repo_csv import load_all as load_restaurant_items 
from app.repositories.track_items_repo_csv import save_all as save_restaurant_items 
"""from app.repositories.order_items_repo import load_all as load_order_items"""
from collections import Counter
from fastapi import HTTPException


def get_stats(data, key):
    idSet = []
    if not data: 
        raise HTTPException(status_code=400,detail=f"No orders yet")
    for item in data:
        if key not in item:
            raise HTTPException(status_code=400,detail=f"Key '{key}' not found in data")
        idSet.append(item[key])
    
    counts = Counter(idSet)
    result = []
    for _id, count in counts.items():
        result.append({key: _id, "count": count})

    return result

def get_stats_on_restaurants():
    orders = load_orders()
    items = load_restaurant_items()
    restaurant_stats = get_stats(orders, "restaurant_id")
    
    for stat in restaurant_stats:
        for item in items:
            if item["restaurant_id"] == stat["restaurant_id"]:
                item["count"] = stat["count"]
    save_restaurant_items(items)

    return restaurant_stats


"""
def get_stats_on_items(restaurant_id=None): will be here 

"""