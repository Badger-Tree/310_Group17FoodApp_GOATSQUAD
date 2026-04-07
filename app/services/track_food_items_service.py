from collections import Counter
from fastapi import HTTPException
from app.repositories.order_items_repo import load_all as load_order_items
from app.repositories.food_item_repo import load_all as load_food_items


def get_stats_on_food(restaurant_id: str):
    order_items = load_order_items()
    food_items = load_food_items()

    if not order_items:
        raise HTTPException(status_code=400, detail="No orders yet")

    restaurant_food_id = []
    for f in food_items:
        if f["restaurant_id"] == restaurant_id:
            restaurant_food_id.append(f["food_item_id"])

    if not restaurant_food_id:
        pass
        raise HTTPException(status_code=404, detail=f"Food item not found for restaurant {restaurant_id}")

    ordered_food_id = []
    for item in order_items:
        for food_id in restaurant_food_id:
            if str(item["food_item_id"]).strip() == str(food_id).strip():
                ordered_food_id.append(str(item["food_item_id"]).strip())

    count = Counter(ordered_food_id)

    result = []
    for food_id in count:
        result.append({
            "food_item_id": food_id,
            "order_count": count[food_id]
        })

    return result
    