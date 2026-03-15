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
    """Allows a restauarant manager or owner to cancel an order
    Input: order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_multi_service(current_user, [UserRole.MANAGER, UserRole.OWNER])
    
    return cancel_order_restaurant_service(orderid)

@router.put("/accept_order",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def accept_order(orderid:str,token: str = Header(...)):
    """Allows a restauarant manager or owner to accept an order. Order status changes to Accepted.
    Input: order id (string)
    Output: OrderResponse (restaurant_id,customer_id,delivery_address_id,delivery_address,cart_id, order_id, created_date, status, total_amount, delivery_id, items)
    """
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_multi_service(current_user, [UserRole.MANAGER, UserRole.OWNER])
    
    return accept_order_service(orderid)