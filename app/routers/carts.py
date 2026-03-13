from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.cart import ListCartResponse, CartResponse, CartBase
from app.services.cart_services import get_items_by_cart, list_carts, create_cart, get_cart_by_id_service

router = APIRouter(prefix="/cart", tags=["carts"])

@router.get("", response_model = List[CartResponse])
def get_cart():
        return list_carts()

@router.get("/by-cart/{cart_id}", response_model=ListCartResponse)
def get_items_by_cart_route(cart_id: str):
    items = get_items_by_cart(cart_id)
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found for cart {cart_id}")
    return items
        

@router.get("/{cart_id}", response_model= CartResponse)
def get_cart_by_id(cart_id: str):
        return get_cart_by_id_service(cart_id)


@router.post("", response_model = CartBase, status_code=201)
def add_cart(cart: CartBase):
        return create_cart(cart.cart_id, cart.customer_id)


