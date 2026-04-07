import random
from typing import List, Optional
from fastapi import HTTPException
from datetime import date, datetime, timezone
from app.repositories.orders_repo import load_all as load_orders, save_all as save_all_orders
from app.repositories.order_items_repo import load_all as load_order_items, save_all as save_all_order_items
from app.schemas.Address import AddressResponse
from app.schemas.Order import OrderHistoryResponse, OrderResponse
from app.schemas.OrderItem import OrderItemResponse # type: ignore
from app.schemas.OrderStatus import OrderStatus
import uuid
from enum import Enum
from app.schemas.cart_schema import CartResponse
from app.services.Delivery_service import create_delivery_service
from app.services.address_service import get_address_by_id_service
from app.services.cart_service import clear_cart, get_cart_by_customer
from app.services.food_item_service import get_food_by_id
from app.services.inventory_service import add_stock, check_availability, subtract_stock
from app.services.notification_service import notify_order_placed, notify_order_status_update, notify_payment_status,notify_refund_issued,notify_order_status_update_customer_cancels
from app.services.payment_service import process_payment_service, process_refund_service
from app.repositories.restaurants_repo_csv import load_all as load_restaurants

def validate_cart(customer_id) -> CartResponse:
    """Checks if a cart exists and returns either an exception or a CartResponse"""
    cart = get_cart_by_customer(customer_id)
    if not cart:
        raise HTTPException(status_code=404, detail="cart not found")
    if not cart.cart_items:
        raise HTTPException(status_code=400, detail="empty cart")
    return cart

def validate_item_inventory(cart):
    for item in cart.cart_items:
        is_available = check_availability(item.food_item_id, item.quantity)
        if is_available == False:
            raise HTTPException(status_code=422, detail="insufficient inventory")
        
def validate_restaurant_from_cart(cart) -> int:
    """gets the restaurant id from the food items in the cart. Items must all be from the same restaurant"""
    first_item = cart.cart_items[0]
    first_food_item = get_food_by_id(first_item.food_item_id)
    restaurant_id = first_food_item["restaurant_id"]

    for item in cart.cart_items:
        food_item = get_food_by_id(item.food_item_id)
        if restaurant_id != food_item["restaurant_id"]:
            raise HTTPException(status_code=400, detail="items not from same restaurant")
    return restaurant_id

def validate_address(address_id) -> AddressResponse:
    """"checks if an address exists, returns AddressResponse or exception"""
    address = get_address_by_id_service(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="address not found")
    return address

def calculate_total(cart):
    """Calculates the total cost of an order given a cart"""
    subtotal = 0.00
    for item in cart.cart_items:
        subtotal += item.price_per_item * item.quantity
    return round(subtotal,2)

def build_order(cart, total_amount, address_id,restaurant_id)->dict:
    """Builds a dictionary with cart and calculated fields needed for an order"""
    order_id = str(uuid.uuid4())
    new_order = {"order_id": order_id,
                "customer_id": cart.customer_id,
                "restaurant_id": restaurant_id,
                "cart_id": cart.cart_id,
                "delivery_id" : None,
                "status" : "PENDING",
                "total_amount" : total_amount,
                "created_date" : datetime.now(timezone.utc),
                "delivery_address_id" : address_id}
    return new_order

def build_order_items(cart, order_id):
    """builds a list of order items from a cart and given order_id"""
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
    return new_items

def handle_payment(order_dict) -> bool:
    """sends an order for payment and then notified customer on result"""
    paid = process_payment_service(order_dict["total_amount"])
    if paid:
        notify_payment_status(order_dict["customer_id"], order_dict["order_id"], True)
        return True
    else:
        notify_payment_status(order_dict["customer_id"], order_dict["order_id"], False)
        raise HTTPException(status_code=400, detail = "payment not processed order")
        
def save_order(new_order: dict):
    """saves an order dict to orders csv using repo methods""" 
    order_data = load_orders()
    order_data.append(new_order)
    save_all_orders(order_data)
    
def save_order_items(new_order_items: dict):
    """saves a dict of order items to order items csv using repo methods"""
    order_item_data = load_order_items()
    for item in new_order_items:
        order_item_data.append(item)
    save_all_order_items(order_item_data)
    
def process_order_service(customer_id: str, address_id:str) -> OrderResponse:
    """receives a cart and asks for payment before creating the order and sending for review. 
    Note that the service is currently using a stub method to get cart."""
    cart = validate_cart(customer_id)
    validate_item_inventory(cart)
    restaurant_id = validate_restaurant_from_cart(cart)
    address = validate_address(address_id)
    total_amount = calculate_total(cart)
    order_dict = build_order(cart, total_amount,address.address_id, restaurant_id)
    order_items_dict = build_order_items(cart, order_dict["order_id"])
    handle_payment(order_dict)
    clear_cart(customer_id, cart.cart_id)
    save_order(order_dict)
    save_order_items(order_items_dict)
    new_order_response = get_order_by_order_id_service(order_dict["order_id"])
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
    raise HTTPException(status_code=404, detail=f"Order notfound")

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

def get_order_status_by_id_service(orderid:str)-> Enum:
    """Method gets a single order mathcing an order id (str)"""
    order_data = load_orders()
    for order in order_data:
        if order.get("order_id") == orderid:
            status_str = order.get("status")
            return OrderStatus(status_str)
    raise HTTPException(status_code=404, detail="Order not found")

def set_order_status_service(order_id:str, new_status:OrderStatus) -> OrderResponse:
    """allows a service to change the status of an order"""
    order_data = load_orders()
    order_item_data = load_order_items()
    for order in order_data:
        if order.get("order_id") == order_id:
            order["status"] = new_status.value
            items_response = []
            for item in order_item_data:
                if item.get("order_id") == order_id:
                    items_response.append(OrderItemResponse(**item))
            save_all_orders(order_data)
            return OrderResponse(**order, items=items_response)
    raise HTTPException(status_code=404, detail=f"Order notfound")       

def cancel_order_customer_service(orderid:str) -> OrderResponse:
    """This method lets a restaurant manager cancel an order. It changes order status to CANCELED"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            if status_enum == OrderStatus.PENDING:
                refunded = process_refund_service(order["total_amount"])
                if refunded: 
                    notify_refund_issued(order["customer_id"], order["order_id"])
                    order["status"] = OrderStatus.CANCELED.value
                    notify_order_status_update_customer_cancels(order["customer_id"], order["order_id"])
                    save_all_orders(order_data)
                    items_responses = []
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            add_stock(food_item_id=item["food_item_id"], quantity=item["quantity"])
                            items_responses.append(OrderItemResponse(**item))
                    return OrderResponse(**order, items = items_responses)
                else:
                    raise HTTPException(status_code=400, detail = "refund not processed")
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")

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
        if order.get("restaurant_id") == str(restaurantid):
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

def cancel_order_restaurant_service(orderid:str) -> OrderResponse:
    """This method lets a restaurant manager cancel an order. It changes order status to CANCELED"""  
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.ACCEPTED or status_enum == OrderStatus.PENDING or status_enum == OrderStatus.OUT_FOR_DELIVERY:
                refunded = process_refund_service(order["total_amount"])
                if refunded:
                    order["status"] = OrderStatus.CANCELED.value
                    notify_refund_issued(order["customer_id"], order["order_id"])
                    notify_order_status_update(order["customer_id"], order["order_id"], False)
                    save_all_orders(order_data)
                    items_responses = []
                    for item in order_item_data:
                        if item.get("order_id") == order.get("order_id"):
                            add_stock(food_item_id=item["food_item_id"], quantity=item["quantity"])
                            items_responses.append(OrderItemResponse(**item))
                    return OrderResponse(**order, items = items_responses)
                else:
                    raise HTTPException(status_code=400, detail = "refund not processed")
            else:
                raise HTTPException(status_code=400, detail = "Cannot cancel order")
    raise HTTPException(status_code=404, detail="Order not found")


def accept_order_service(orderid:str) -> OrderResponse:
    """Method used by restaurant manager to accept an order. It changes order status from PENDING to ACCEPTED"""
    order_data = load_orders()
    order_item_data = load_order_items()
    
    for order in order_data:
        if order.get("order_id") == orderid:   
            
            status_str = order.get("status")
            status_enum = OrderStatus(status_str)
            
            if status_enum == OrderStatus.PENDING:
                order["status"] = OrderStatus.ACCEPTED.value
                notify_order_status_update(order["customer_id"], order["order_id"], True)
                # create delivery
                delivery = create_delivery_service(order)
                order["delivery_id"] = delivery.delivery_id

                save_all_orders(order_data)
                items_responses = []
                
                for item in order_item_data:
                    if item.get("order_id") == order.get("order_id"):
                        subtract_stock(item["food_item_id"], quantity=item["quantity"])
                        items_responses.append(OrderItemResponse(**item))
                return OrderResponse(**order, items = items_responses)
            else:
                raise HTTPException(status_code=400, detail = "Cannot accept order")
    raise HTTPException(status_code=404, detail="Order not found")


#Order History feature by Tesh
def get_order_history_service(
        customer_id: str, 
        restaurant = None, 
        cuisine = None, 
        accepted = None, 
        sort_by="date", 
        sort_order="desc",
        date = None
        )-> List[OrderHistoryResponse]:
    """Method gets a list of OrderResponse objects matching to the currently logged in user and displays their previous orders"""
   
    orders = load_orders()
    order_items = load_order_items()
    restaurants = load_restaurants()

    filtered_orders = filter_order_history_by_customer_id(orders, customer_id)

    order_history = []

    for order in filtered_orders:
        restaurant_info = next(
            (r for r in restaurants 
                if str(r["restaurant_id"]) == str(order["restaurant_id"])), None
             )
        
        if restaurant_info is None:
            continue

        items_response = []
        for item in order_items:
            if item.get("order_id") == order.get("order_id"):
                items_response.append(OrderItemResponse(**item))
        
        order_history_response = OrderHistoryResponse(
            **order,
            items = items_response,
            restaurant_name = restaurant_info["restaurant_name"],
            cuisine = restaurant_info["cuisine"]
        )

        order_history.append(order_history_response)
    
    if restaurant:
        order_history = filter_order_history_by_restaurant(order_history, restaurant)
    
    if cuisine:
        order_history = filter_order_history_by_cuisine(order_history, cuisine)

    if date is not None:
        order_history = filter_order_history_by_date(order_history, date)
    
    if accepted is not None:
        order_history = filter_order_history_by_accepted(order_history, accepted)
    
    if sort_by == "restaurant":
        order_history = sort_order_history_by_restaurant(order_history, sort_order)
    elif sort_by == "cuisine":
        order_history = sort_order_history_by_cuisine(order_history, sort_order)
    else:
         order_history = sort_order_history_by_date(order_history, sort_order)  
        
    return order_history


    

#Helper functions
def filter_order_history_by_customer_id(orders, customer_id):
    customer_orders = []
    for order in orders:
        if order.get("customer_id") == customer_id:
            customer_orders.append(order)
    return customer_orders

def filter_order_history_by_restaurant(orders, restaurant):
    restaurant_orders = []
    for order in orders:
        if restaurant.lower().strip() in order.restaurant_name.lower().strip():
            restaurant_orders.append(order)
    return restaurant_orders

def sort_order_history_by_restaurant(orders, sort_order):
    
    if sort_order is None or sort_order.lower().strip() == "asc":
        sorted_orders = sorted(orders, key=lambda x: x.restaurant_name.lower().strip())
    elif sort_order.lower().strip() == "desc":
        sorted_orders = sorted(orders, key=lambda x: x.restaurant_name.lower().strip(), reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")
    return sorted_orders
    
def filter_order_history_by_cuisine(orders, cuisine):
    cuisine_orders = []
    for order in orders:
        if order.cuisine.lower().strip() == cuisine.lower().strip():
            cuisine_orders.append(order)
    return cuisine_orders

def sort_order_history_by_cuisine(orders, sort_order):
    
    if sort_order is None or sort_order.lower().strip() == "asc":
        sorted_orders = sorted(orders, key=lambda x: x.cuisine.lower().strip())
    elif sort_order.lower().strip() == "desc":
        sorted_orders = sorted(orders, key=lambda x: x.cuisine.lower().strip(), reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")
    return sorted_orders

def filter_order_history_by_date(orders, date):
    date_orders = []
    for order in orders:
        if order.created_date.date() == date:
            date_orders.append(order)
    return date_orders

def sort_order_history_by_date(orders, sort_order):
    
    if sort_order is None or sort_order.lower().strip() == "asc":
        sorted_orders = sorted(orders, key=lambda x: x.created_date)
    elif sort_order.lower().strip() == "desc":
        sorted_orders = sorted(orders, key=lambda x: x.created_date, reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")
    return sorted_orders

def filter_order_history_by_accepted(orders, accepted):
    accepted_orders = []
    for order in orders:
        if accepted and order.status == OrderStatus.ACCEPTED:
            accepted_orders.append(order)
        elif not accepted and order.status != OrderStatus.ACCEPTED:
            accepted_orders.append(order)
    return accepted_orders



