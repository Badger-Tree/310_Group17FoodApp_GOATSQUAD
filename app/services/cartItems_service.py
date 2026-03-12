import uuid
from typing import List
from fastapi import HTTPException
from app.schemas.cartItem import CartItemUpdate, CartItemResponse
from app.repositories.cartItems_repo import load_all, save_all
from decimal import Decimal

def update_cartItem(cart_item_id: str, payload: CartItemUpdate) -> CartItemResponse:
    cart_items_data = load_all()
    updated = None
    quantity = int(payload["quantity"])
    if quantity <= 0:
        raise ValueError("Quantity cannot be zero")
    
    price_per_item = float(payload["price_per_item"])
    if price_per_item <= 0:
        raise ValueError("Price cannot be zero")
    
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            
            subtotal = float(quantity*price_per_item)
            updated = {
                "cart_item_id": str(cart_item_id),
                "cart_id": str(it.get("cart_id")), 
                "food_item_id": int(it.get("food_item_id")), 
                "quantity": int(quantity),
                "price_per_item": float(price_per_item), 
                "subtotal": float(subtotal)
                }
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

