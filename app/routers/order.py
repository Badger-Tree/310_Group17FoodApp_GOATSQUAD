<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, status
from app.schemas.Order import OrderCreate, OrderResponse
from app.services.order_service import create_order_service, get_order_by_order_id_service,get_orders_by_restaurant_service,get_orders_by_userid_service,get_order_status_by_id_service,cancel_order_customer_service,cancel_order_restaurant_service,accept_order_service
from typing import List
from enum import Enum
from app.schemas.Order import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/create_order", response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    """Creates and saves and order given an OrderCreate. Gets order items from cart
    Input: OrderCreate as payload (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    return create_order_service(payload)

@router.get("/get_order_by_id", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(orderid: str):
    """Finds an order given an order id (string)
    Input: Order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    return get_order_by_order_id_service(orderid)

@router.get("/get_order_by_restaurant", response_model = List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders_by_restaurant(restaurant_id:int):
    """Finds any orders associated with a restaurantid (string), return list
    Input: restaurant id (int)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    return get_orders_by_restaurant_service(restaurant_id)

@router.get("/get_order_by_user", response_model = List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders_by_userid(userid:str):
    """Finds any orders associated with a userid (string), return list
    Input: user id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    return get_orders_by_userid_service(userid)

@router.get("/order_status", response_model = Enum, status_code=status.HTTP_200_OK)
def get_order_status_by_id(orderid:str):
    """Returns an order status enum given an order id str
    Input: order id (string)
    Output: OrderStatus (PENDING,APPROVED,CANCELED,IN_PREPARATION,OUT_FOR_DELIVERY,COMPLETED)
    """
    return get_order_status_by_id_service(orderid)

@router.put("/cancel_order_customer",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order_customer(orderid:str):
    """Allows a customer to cancel an order
    Input: order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    return cancel_order_customer_service(orderid)

@router.put("/cancel_order_restaurant",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order_restaurant(orderid:str):
=======
from fastapi import APIRouter, HTTPException, Header, status
from app.schemas.Order import OrderCreate, OrderResponse
from app.schemas.Role import UserRole
from app.schemas.Token import Token
from app.services.order_service import cancel_order_restaurant_service,accept_order_service
from typing import List
from enum import Enum
from app.schemas.Order import OrderResponse
from app.services.session_manager_service import get_user_from_session
from app.services.authorization_service import require_role_multi_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.put("/cancel_order_restaurant",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order_restaurant(orderid:str,token: str = Header(...)):
>>>>>>> main
    """Allows a restauarant manager or owner to cancel an order
    Input: order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
<<<<<<< HEAD
    return cancel_order_restaurant_service(orderid)

@router.put("/accept_order",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def accept_order(orderid:str):
=======
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_multi_service(current_user, [UserRole.MANAGER, UserRole.OWNER])
    
    return cancel_order_restaurant_service(orderid)

@router.put("/accept_order",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def accept_order(orderid:str,token: str = Header(...)):
>>>>>>> main
    """Allows a restauarant manager or owner to accept an order. Order status changes to Accepted.
    Input: order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
<<<<<<< HEAD
=======
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_multi_service(current_user, [UserRole.MANAGER, UserRole.OWNER])
    
>>>>>>> main
    return accept_order_service(orderid)