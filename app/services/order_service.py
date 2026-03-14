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

from app.services.payment_service import process_refund_service

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
                    order["status"] = OrderStatus.CANCELED.value
                    save_all_orders(order_data)
                    items_responses = []
                    
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            items_responses.append(OrderItemResponse(**item))
                    return OrderResponse(**order, items = items_responses)
                raise HTTPException(status_code=400, detail = "refund not processed")
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")