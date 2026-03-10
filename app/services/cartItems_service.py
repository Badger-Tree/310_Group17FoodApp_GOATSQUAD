import uuid
from typing import List
from fastapi import HTTPException
from app.schemas.cartItem import CartItemAdd, CartItemUpdate, CartItemResponse
from app.repositories.cartItems_repo import load_all, save_all



def get_cartItem_by_id(cart_item_id: str) -> CartItemResponse:
    cart_items_data = load_all()
    for it in cart_items_data:
        if it.get("cart_item_id") == cart_item_id:
            return CartItemResponse(**it)
    raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")

def get_items_by_cart(cart_id: str) -> List[CartItemResponse]:
    cart_items_data = load_all()
    cart_items_responses = []
    
    for it in cart_items_data:
        if it.get("cart_id") == cart_id:
            cart_items_responses.append(CartItemResponse(**it))
    if not cart_items_responses:
        raise HTTPException(status_code=404, detail=f"Cart'{cart_id}' not found")
    return cart_items_responses

def add_cartItem(payload: CartItemAdd) -> CartItemResponse:
    cart_items_data = load_all()
    new_id = str(uuid.uuid4())
    if any(it.get("cart_item_id") == new_id for it in cart_items_data):
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    
    cart = load_all()
    cart_exists = False
    for c in cart:
        if c["cart_id"] == payload.cart_id.strip():
            cart_exists = True
            break
        if not cart_exists:
            raise HTTPException(status_code=404, detail=f"User {payload.cart_id} not found")

    new_cart_item = {
        "cart_item_id": new_id,
        "cart_id": payload.cart_id.strip(),
        "food_item_id": payload.food_item_id.strip(),
        "quantity": payload.quantity.strip(),
        "price_per_item": payload.price_per_item.strip()
    }

    cart_items_data.append(new_cart_item)
    save_all(cart_items_data)
    return CartItemResponse(**new_cart_item)


def update_cartItem(cart_item_id: str, payload: CartItemUpdate) -> CartItemResponse:
    cart_items_data = load_all()
    updated = None
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            updated = {
                "cart_item_id": cart_item_id,
                "cart_id": it.get("cart_id"), 
                "food_item_id": it.get("food_item_id"), 
                "quantity": payload.quantity.strip(), 
                "price_per_item": payload.price_per_item.strip() }
            cart_items_data[idx] = updated
            break
    if not updated: 
            raise HTTPException(status_code=404, detail=f"Cart Item '{cart_item_id}' not found")
    save_all(cart_items_data)
    return CartItemResponse(**updated)
    

def remove_cartItem(cart_item_id: str) -> None:
    cart_items_data = load_all()
    found_cart_item = False
    for i, cart in enumerate(cart_items_data):
        if cart.get("cart_item_id") == cart_item_id:
            found_cart_item = True
            cart_items_data.pop(i)
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")
    save_all(cart_items_data)

