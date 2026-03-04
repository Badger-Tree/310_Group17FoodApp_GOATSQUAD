from typing import List
from fastapi import HTTPException
from datetime import datetime
from app.repositories.orders_repo import load_all as load_orders, save_all as save_all_orders
from app.repositories.order_items_repo import load_all as load_order_items, save_all as save_all_order_items
from app.schemas.Order import OrderResponse, OrderCreate
from app.schemas.OrderItem import OrderItemCreate, OrderItemResponse # type: ignore


from app.schemas.OrderStatus import OrderStatus
import uuid


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

def create_order_service(order_input: OrderCreate) -> OrderResponse:
    order_data = load_orders()
    order_item_data = load_order_items()
    
    order_id = str(uuid.uuid4())
    for orders in order_data:
        if orders["order_id"] == order_id:
               raise HTTPException(status_code=409, detail="ID collision; retry.")
    total = 0.00
    for item in order_input.items:
        total += item.price_per_item * item.quantity
    
    new_order = {"order_id": order_id,
                "customer_id": order_input.customer_id,
                "restaurant_id": order_input.restaurant_id,
                "cart_id": order_input.cart_id,
                "delivery_id" : 0,
                "status" : "PENDING",
                "total_amount" : round(total,2),
                "created_date" : datetime.utcnow().isoformat()}
    order_data.append(new_order)
    save_all_orders(order_data)
    
    new_items = []
    for item in order_input.items:
        new_item = {
            "order_item_id": str(uuid.uuid4()),
            "order_id": order_id,
            "food_item_id":item.food_item_id,
            "quantity": item.quantity,
            "price_per_item": item.price_per_item
            }
        order_item_data.append(new_item)
        new_items.append(OrderItemResponse(**new_item))
        
    save_all_order_items(order_item_data)
           
    return OrderResponse(order_id= order_id,
                         customer_id= order_input.customer_id, 
                         restaurant_id= order_input.restaurant_id,
                         delivery_id = "",
                         status = "PENDING",
                         total_amount = round(total,2),
                         created_date = datetime.utcnow().isoformat(),
                         items=new_items)
    
def get_order_by_order_id_service(orderid:str)-> OrderResponse | None:
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:
            items_response = []
            for item in order_item_data:
                if item.get("order_id") == orderid:
                    items_response.append(OrderItemResponse(**item))

            return OrderResponse(**order, items=items_response)
    return None

def get_orders_by_restaurant_service(restaurantid:str)-> List[OrderResponse] | None:
    order_data = load_orders()
    order_item_data = load_order_items()
    
    order_responses = []
    for order in order_data:
        if order.get("restaurant_id") == restaurantid:
            items_responses = []
            for item in order_item_data:
                if item.get("order_id") == order.get("order_id"):
                    items_responses.append(OrderItemResponse(**item))
            order_responses.append(OrderResponse(**order, items = items_responses))

    if not order_responses:
        return None
    return order_responses

def get_orders_by_userid_service(userid:str)-> OrderResponse | None:
    order_data = load_orders()
    order_item_data = load_order_items()
    
    order_responses = []
    for order in order_data:
        if order.get("customer_id") == userid:
            items_responses = []
            for item in order_item_data:
                if item.get("order_id") == order.get("order_id"):
                    items_responses.append(OrderItemResponse(**item))
            order_responses.append(OrderResponse(**order, items = items_responses))

    if not order_responses:
        return None
    return order_responses