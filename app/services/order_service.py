from typing import List
from fastapi import HTTPException
from app.repositories.orders_repo import load_all as load_orders, save_all as save_all_orders
from app.repositories.order_items_repo import load_all as load_order_items, save_all as save_all_order_items
from app.schemas.Order import OrderResponse
from app.schemas.OrderItem import OrderItemResponse


## test to show all orders, wont be in final app

def list_all_orders() -> List[OrderResponse]:
    order_data = load_orders()
    order_item_data = load_order_items()
    order_responses = []
    for order in order_data:
        items = []
        for item in order_item_data:
            if item["order_id"] == order["order_id"]:
                items.append(OrderItemResponse(**item))
        order["items"] = items
        order_responses.append(OrderResponse(**order))
    return order_responses