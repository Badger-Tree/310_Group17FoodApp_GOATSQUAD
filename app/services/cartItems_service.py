import uuid
from fastapi import HTTPException
from app.schemas.cartItem import CartItemResponse
from app.repositories.cartItems_repo import load_all

def get_cartItem_by_id(cart_item_id: str) -> CartItemResponse:
    cart_items_data = load_all()
    cart_item_id = str(cart_item_id).strip()
    if not cart_item_id:
        raise HTTPException(status_code=400, detail="cart_item_id cannot be empty")
    for it in cart_items_data:
        if it.get("cart_item_id") == cart_item_id:
            return CartItemResponse(**it).model_dump()
    raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")

