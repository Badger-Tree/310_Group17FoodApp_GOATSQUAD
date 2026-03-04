from fastapi import APIRouter, HTTPException, status
from app.schemas.Order import OrderCreate, OrderResponse
from app.services.order_service import create_order_service, get_order_by_order_id_service,get_orders_by_restaurant_service,get_orders_by_userid_service,get_order_status_by_id_service,set_order_status_service,cancel_order_customer_service,cancel_order_restaurant_service
from typing import List
from enum import Enum

from app.schemas.Order import OrderResponse
from app.services.order_service import list_all_orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_orders():
    orders = list_all_orders()
    return orders

@router.post("/create_order", response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(order_input: OrderCreate):
    return create_order_service(order_input)

@router.get("/get_order_by_id", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(orderid: str):
    return get_order_by_order_id_service(orderid)

@router.get("/get_order_by_restaurant", response_model = List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders_by_restaurant(restuarantid:str):
    return get_orders_by_restaurant_service(restuarantid)

@router.get("/get_order_by_user", response_model = List[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders_by_userid(userid:str):
    return get_orders_by_userid_service(userid)

@router.get("/order_status", response_model = Enum, status_code=status.HTTP_200_OK)
def get_order_status_by_id(orderid:str):
    return get_order_status_by_id_service(orderid)

@router.put("/update_order_status", response_model = OrderResponse, status_code=status.HTTP_200_OK)
def set_order_status(orderid:str, status:str):
    return set_order_status_service(orderid, status)

@router.put("/cancel_order_customer",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order_customer(orderid:str):
    return cancel_order_customer_service(orderid)

@router.put("/cancel_order_restaurant",response_model = OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order_restaurant(orderid:str):
    return cancel_order_restaurant_service(orderid)