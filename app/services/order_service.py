from typing import List
from fastapi import HTTPException
from datetime import datetime
from app.repositories.orders_repo import load_all as load_orders, save_all as save_all_orders
from app.repositories.order_items_repo import load_all as load_order_items, save_all as save_all_order_items
from app.schemas.Order import OrderResponse, OrderCreate
from app.schemas.OrderItem import OrderItemResponse # type: ignore
from enum import Enum
from app.schemas.OrderStatus import OrderStatus
import uuid


def create_order_service(order_input: OrderCreate) -> OrderResponse:
    """Method Creates an Order from a cart"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    # this is using a stub to get cart data
    cart = get_cart_by_id(order_input.cart_id)
    if not cart.cart_items:
        raise HTTPException(status_code=400, detail="cart is empty")
    
    order_id = str(uuid.uuid4())
    for orders in order_data:
        if orders["order_id"] == order_id:
               raise HTTPException(status_code=409, detail="ID collision; retry.")
           
    subtotal = 0.00
    
    for item in cart.cart_items:
        subtotal += item.price_per_item * item.quantity
    
    ## the fees will come from restuarant service when it is built
    fees = temp_get_restaurant_fee(order_input.restaurant_id)
    
    total_amount = round(subtotal + fees, 2)
    
    new_order = {"order_id": order_id,
                "customer_id": cart.customer_id,
                "restaurant_id": cart.restaurant_id,
                "cart_id": cart.cart_id,
                "delivery_id" : None,
                "status" : "PENDING",
                "total_amount" : total_amount,
                "created_date" : datetime.utcnow().isoformat(),
                "delivery_address_id" : cart.delivery_address_id}
    order_data.append(new_order)
    save_all_orders(order_data)
    
 
    new_items = []
    for item in cart.cart_items:
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
                         customer_id= cart.customer_id, 
                         restaurant_id= cart.restaurant_id,
                         delivery_id = None,
                         status = "PENDING",
                         total_amount = total_amount,
                         created_date = new_order["created_date"],
                         items = new_items)
    
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

def get_orders_by_restaurant_service(restaurantid:str)-> List[OrderResponse] | None:
    """Method gets list of Order Response objects matching to a restaurant id. Takes in restaurant id"""
    # should check on Tesh's pull to see what type the restaurant id is, probably int
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

    if not order_responses:
        return None
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
    ##this will also need to request payment refund
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.PENDING:
                order["status"] = OrderStatus.CANCELED.value
                save_all_orders(order_data)
                items_responses = []
                
                for item in order_item_data:
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            items_responses.append(OrderItemResponse(**item))
                return OrderResponse(**order, items = items_responses)
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")

def cancel_order_restaurant_service(orderid:str) -> OrderResponse:
    """This method lets a restaurant manager cancel an order. It changes order status to CANCELED"""
    ##this will also need to request payment refund
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.APPROVED or status_enum == OrderStatus.PENDING or status_enum == OrderStatus.OUT_FOR_DELIVERY or status_enum == OrderStatus.IN_PREPARATION:
                order["status"] = OrderStatus.CANCELED.value
                save_all_orders(order_data)
                items_responses = []
                
                for item in order_item_data:
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            items_responses.append(OrderItemResponse(**item))
                return OrderResponse(**order, items = items_responses)
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
def temp_get_restaurant_fee(restaurant_id: str) -> float:
    """
    Temporary placeholder until restaurant service is created
    """
    return 1.00
def get_cart_by_id(cart_id: str):
    class TempCart:
        def __init__(self):
            self.cart_id = cart_id
            self.customer_id = "123"
            self.restaurant_id = "456"
            self.delivery_address_id = "1"
            self.cart_items = [TempCartItem("food1", 1, 4.00),
                               TempCartItem("food2", 5, 1.20),
                               TempCartItem("food3", 2, 2.00),                  
            ]
    class TempCartItem:
        def __init__(self, food_item_id, quantity, price_per_item):
            self.food_item_id = food_item_id
            self.quantity = quantity
            self.price_per_item = price_per_item
    return TempCart()