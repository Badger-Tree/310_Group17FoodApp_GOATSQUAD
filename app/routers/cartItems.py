from fastapi import APIRouter, status
from app.schemas.cartItem import CartItemUpdate, CartItemResponse
from app.services.cartItems_service import update_cartItem, remove_cartItem

router = APIRouter(prefix="/cart-items", tags=["cartItems"])


@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: str, payload: CartItemUpdate):
    return update_cartItem(cart_item_id, payload)

@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(cart_item_id: str):
    remove_cartItem(cart_item_id)
    return None