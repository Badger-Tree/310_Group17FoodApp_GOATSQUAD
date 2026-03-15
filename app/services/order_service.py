import random
from typing import List
from fastapi import HTTPException
from datetime import datetime, timezone
from app.repositories.orders_repo import load_all as load_orders, save_all as save_all_orders
from app.repositories.order_items_repo import load_all as load_order_items, save_all as save_all_order_items
from app.schemas.Order import OrderResponse, OrderCreate
from app.schemas.OrderItem import OrderItemResponse # type: ignore
from app.schemas.OrderStatus import OrderStatus
import uuid
from enum import Enum
from app.services.notification_service import notify_order_placed, notify_order_status_update, notify_payment_status
from app.services.payment_service import process_payment_service, process_refund_service

def process_order_service(cart_id: str):
    """receives a cart and asks for payment before creating the order and sending for review. 
    Note that the service is currently using a stub method to get cart."""
    cart = get_cart_by_id(cart_id)
    if not cart.cart_items:
        raise HTTPException(status_code=400, detail="cart is empty")
    
    order_id = str(uuid.uuid4())
    
    subtotal = 0.00
    for item in cart.cart_items:
        subtotal += item.price_per_item * item.quantity
    total_amount = round(subtotal,2)
    new_order = {"order_id": order_id,
                "customer_id": cart.customer_id,
                "restaurant_id": cart.restaurant_id,
                "cart_id": cart.cart_id,
                "delivery_id" : None,
                "status" : "PENDING",
                "total_amount" : total_amount,
                "created_date" : datetime.now(timezone.utc),
                "delivery_address_id" : cart.delivery_address_id}

    new_items = []
    for item in cart.cart_items:
        new_item = {
            "order_item_id": str(uuid.uuid4()),
            "order_id": order_id,
            "food_item_id":item.food_item_id,
            "quantity": item.quantity,
            "price_per_item": item.price_per_item
            }
        new_items.append(new_item)

    paid = process_payment_service(total_amount)
    if paid:
        new_order = create_order_service(new_order,new_items)
        notify_payment_status(cart.customer_id, order_id, True)
        return new_order
    else:
        notify_payment_status(cart.customer_id, order_id, False)
        raise HTTPException(status_code=400, detail = "payment not processed order")

        
def create_order_service(new_order: dict, new_items: list[dict]) -> OrderResponse:
    """Method Creates an Order from a dictionary after if was processed for payment"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    order_data.append(new_order)
    save_all_orders(order_data)
    
    new_items_response = []
    for item in new_items:
        order_item_data.append(item)
        new_items_response.append(OrderItemResponse(**item))
        
    save_all_order_items(order_item_data)
    
    new_order_response =OrderResponse(order_id= new_order["order_id"],
                        customer_id= new_order["customer_id"],
                        restaurant_id= new_order["restaurant_id"],
                        delivery_id = None,
                        delivery_address_id=new_order["delivery_address_id"],
                        status = OrderStatus.PENDING,
                        total_amount = new_order["total_amount"],
                        created_date = new_order["created_date"],
                        items = new_items_response)
    
    notify_order_placed(new_order_response.customer_id, new_order_response.restaurant_id, new_order_response.order_id)
    return new_order_response
    
def get_order_by_order_id_service(orderid:str)-> OrderResponse | None:
    """Method gets a single OrderResponse object. Takes in an order id (str)"""
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

def get_orders_by_restaurant_service(restaurantid:int)-> List[OrderResponse]:
    """Method gets list of Order Response objects matching to a restaurant id. Takes in restaurant id"""
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
    return order_responses

def get_orders_by_userid_service(userid:str)-> List[OrderResponse]:
    """Method gets list of OrderResponse objects. Takes in userid (str)"""
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
    return order_responses

def get_order_status_by_id_service(orderid:str)-> Enum | None:
    """Method gets a single order mathcing an order id (str)"""
    order_data = load_orders()
    for order in order_data:
        if order.get("order_id") == orderid:
            status_str = order.get("status")
            return OrderStatus(status_str)
    return None
        
def cancel_order_customer_service(orderid:str) -> OrderResponse:
    """This method lets a customer cancel an order. It changes order status to CANCELED"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            if status_enum == OrderStatus.PENDING:
                refunded = process_refund_service(order["total_amount"])
                if refunded: 
                    notify_payment_status(order.customer_id, order.order_id, True)
                    order["status"] = OrderStatus.CANCELED.value
                    notify_order_status_update(order.customer_id, order.order_id, False)
                    save_all_orders(order_data)
                    items_responses = []
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            items_responses.append(OrderItemResponse(**item))
                    return OrderResponse(**order, items = items_responses)
                else:
                    notify_payment_status(order.customer_id, order.order_id, False)
                    raise HTTPException(status_code=400, detail = "refund not processed")
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")

def cancel_order_restaurant_service(orderid:str) -> OrderResponse:
    """This method lets a restaurant manager cancel an order. It changes order status to CANCELED"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.APPROVED or status_enum == OrderStatus.PENDING or status_enum == OrderStatus.OUT_FOR_DELIVERY or status_enum == OrderStatus.IN_PREPARATION:
                refunded = process_refund_service(order["total_amount"])
                if refunded:
                    order["status"] = OrderStatus.CANCELED.value
                    notify_payment_status(order.customer_id, order.order_id, True)
                    notify_order_status_update(order.customer_id, order.order_id, False)
                    save_all_orders(order_data)
                    items_responses = []
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            items_responses.append(OrderItemResponse(**item))
                    return OrderResponse(**order, items = items_responses)
                else:
                    notify_payment_status(order.customer_id, order.order_id, False)
                    raise HTTPException(status_code=400, detail = "refund not processed")
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")

def accept_order_service(orderid:str) -> OrderResponse:
    """Method used by restaurant manager to accept an order. It changes order status from PENDING to APPROVED"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.PENDING:
                order["status"] = OrderStatus.APPROVED.value
                save_all_orders(order_data)
                items_responses = []
                
                for item in order_item_data:
                    if item.get("order_id") == order.get("order_id"):
                        items_responses.append(OrderItemResponse(**item))
                return OrderResponse(**order, items = items_responses)
            else:
                raise HTTPException(status_code=400, detail = "Cannot accept order")
    raise HTTPException(status_code=404, detail="Order not found")

##################################################################
# Stub methods that will get replaced when real modules are availble
##################################################################

from pydantic import BaseModel
from typing import List

class CartItemResponse(BaseModel):
    food_item_id: int
    quantity: int
    price_per_item: float


class CartResponse(BaseModel):
    cart_id: str
    customer_id: str
    restaurant_id: str
    delivery_address_id: str
    cart_items: List[CartItemResponse]
    
def get_cart_by_id(cart_id: str) -> CartResponse:

    cart_items = [
        CartItemResponse(
            food_item_id=1,
            quantity=1,
            price_per_item=1.00
        )
    ]

    cart = CartResponse(
        cart_id=cart_id,
        customer_id="1",
        restaurant_id="1",
        delivery_address_id="1",
        cart_items=cart_items
    )

    return cart