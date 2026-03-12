from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.cart import ListCartResponse
from app.services.cart_service import get_items_by_cart

router = APIRouter(prefix="/cart", tags=["carts"])

@router.get("/by-cart/{cart_id}", response_model=ListCartResponse)
def get_items_by_cart_route(cart_id: str):
    print(f"Requested cart_id: {cart_id}")
    items = get_items_by_cart(cart_id)
    print(f"Items returned from service: {items}")
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found for cart {cart_id}")
    return items