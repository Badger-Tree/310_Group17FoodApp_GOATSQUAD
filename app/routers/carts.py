from fastapi import APIRouter, status
from typing import List
from app.schemas.cart import CartResponse, CartBase
from app.services.cart_services import get_items_by_cart, list_carts, create_cart, get_cart_by_id_service

router = APIRouter(prefix="/cart", tags=["carts"])

@router.get("", response_model = List[CartResponse])
def get_cart():
        """Gets a list of Cart Response"""
        return list_carts()

@router.get("/{cart_id}", response_model= CartBase)
def get_cart_by_id(cart_id: str):
        """Gets a cart by its cart id and returns a CartBase"""
        return get_cart_by_id_service(cart_id)

@router.get("/by-cart/{cart_id}", response_model=dict)
def get_items_by_carts(cart_id: str):
        """Gets all items of a cart with the cart id and returns a dictionary of data"""
        return get_items_by_cart(cart_id)

@router.post("", response_model = CartBase, status_code=201)
def add_cart(cart: CartBase):
        """Creates a new cart with CartBase data"""
        return create_cart(cart.cart_id, cart.customer_id)

"""
@router.clear("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_carts(cart_item_id: str):
    clear_cart(cart_item_id)
    return None
"""