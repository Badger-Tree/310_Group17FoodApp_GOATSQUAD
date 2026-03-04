from fastapi import APIRouter
from typing import List
from app.schemas.carts import CartResponse, CartBase
from app.services.cart_services import list_carts, create_cart, get_cart_by_id_service

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("", response_model = List[CartResponse])
def get_cart():
        return list_carts()
        

@router.get("/{cart_id}", response_model= CartResponse)
def get_cart_by_id(cart_id: str):
        return get_cart_by_id_service(cart_id)


@router.post("", response_model = CartBase, status_code=201)
def add_cart(cart: CartBase):
        return create_cart(cart.cart_id, cart.customer_id)
        
               
        



