from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.Order import OrderResponse
from app.services.order_service import list_all_orders

router = APIRouter(prefix="/users", tags=["orders"])

@router.get("", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_orders():
    orders = list_all_orders()
    return orders