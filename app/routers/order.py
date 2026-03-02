from fastapi import APIRouter, HTTPException, status
from app.schemas.Order import OrderCreate, OrderResponse
from app.services.order_service import create_order_service
from typing import List


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

