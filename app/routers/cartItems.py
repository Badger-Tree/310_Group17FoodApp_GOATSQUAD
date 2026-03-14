from fastapi import APIRouter, status
from typing import List
from app.schemas.cartItem import CartItemAdd, CartItemResponse
from app.services.cartItems_service import add_cart_item

router = APIRouter(prefix="/cart-items", tags=["cartItems"])

@router.post("/", response_model=CartItemResponse, status_code=201)
def add_cart_item_route(item: CartItemAdd):
    """Creates a cart with provided data and returns cart information"""
    return add_cart_item(item)
