import uuid
from typing import List
from fastapi import HTTPException
from app.schemas.cart import ListCartResponse
from app.repositories.cartItems_repo import load_all, save_all


def get_items_by_cart(cart_id: str) -> List[ListCartResponse]:
    cart_items_data = load_all()
    cart_id = str(cart_id).strip()
    if not cart_id: 
        raise HTTPException(status_code=400, detail="cart_id cannot be empty")
   
    cart_items_responses = []
    calculateSubtotal = 0
    
    for cart in cart_items_data:
        for it in cart.get("cartList", []):
            if str(it.get("cart_id"))== cart_id:
                cart_item_id = it.get("cart_item_id")
                food_item_id = int(it.get("food_item_id"))
                price_per_item = float(it.get("price_per_item"))
                quantity = int(it.get("quantity"))
                subtotal = float(it.get("subtotal"))
                
                cart_items_responses.append({
                "cart_item_id": cart_item_id,
                "cart_id": cart_id,
                "food_item_id": food_item_id,
                "quantity": quantity,
                "price_per_item": price_per_item,
                "subtotal": subtotal
            })
            calculateSubtotal += float(it.get("subtotal"))
            

    if not cart_items_responses:
        raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found")
    
    return { 
        "cartList": cart_items_responses,
        "total": calculateSubtotal
    }
    