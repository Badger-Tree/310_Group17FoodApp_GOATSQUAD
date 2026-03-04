from fastapi import APIRouter, status
import uuid
from typing import List
from app.schemas.cartItem import CartItemAdd, CartItemUpdate, CartItemResponse
from app.services.cartItems_service import update_cartItem, remove_cartItem, get_cartItem_by_id, get_items_by_cart, add_cart_item

router = APIRouter(prefix="/cart-items", tags=["cartItems"])

@router.get("/by-id/{cart_item_id}", response_model = CartItemResponse)
def get_cart_item_id(cart_item_id: str):
        return get_cartItem_by_id(cart_item_id)

@router.get("/by-cart/{cart_id}", response_model=List[CartItemResponse])
def get_items_by_cart_route(cart_id: str):
    return get_items_by_cart(cart_id)

@router.post("/", response_model=CartItemResponse, status_code=201)
def add_cart_item_route(item: CartItemAdd):
    return add_cart_item(item)

@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: str, payload: CartItemUpdate):
    return update_cartItem(cart_item_id, payload)

@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(cart_item_id: str):
    remove_cartItem(cart_item_id)
    return None