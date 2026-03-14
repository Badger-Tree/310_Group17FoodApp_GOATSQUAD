import uuid
from typing import List
from fastapi import HTTPException
from app.schemas.cart import ListCartResponse, CartResponse
from app.repositories.cart_repo import load_all, save_all

def list_carts() -> List[CartResponse]:
    return [CartResponse(**it) for it in load_all()]

def get_cart_by_id_service(cart_id : str) -> CartResponse:
    from app.repositories.cartItems_repo import load_all as load_all_cart_items
    cart_data = load_all()
    item_data = load_all_cart_items()
    cart_response = []
    for it in cart_data:
        if it.get("cart_id") == cart_id:
            subtotal = 0
            for item in item_data:
                if item.get("cart_id") == cart_id:
                    cart_response.append(item)
                    subtotal += item.get("quantity") * item.get("price_per_item")

            return CartResponse(
               items = cart_response,
               subtotal = subtotal
            )
    raise HTTPException(status_code=404, detail=f"Item '{cart_id}' not found")

def get_items_by_cart(cart_id: str) -> List[ListCartResponse]:
    cart_items_data = load_all()
    cart_id = cart_id.strip()
    if not cart_id: 
        raise HTTPException(status_code=400, detail="cart_id cannot be empty")
   
    cart_items_responses = []
    calculateSubtotal = 0
    
    for cart in cart_items_data:
        for it in cart.get("cartList"):
            if it.get("cart_id")== cart_id:
                cart_item_id = it.get("cart_item_id")
                food_item_id = it.get("food_item_id")
                price_per_item = float(it.get("price_per_item"))
                quantity = it.get("quantity")
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

def create_cart(cart_id: str, customer_id: str):
    cart_data = load_all()
    cart_id = cart_id.strip()
    customer_id = cart_id.strip()
   
    new_cart = {
        "cart_id": cart_id,
        "customer_id": customer_id
    }
   
    cart_data.append(new_cart)
    save_all(cart_data)
    return new_cart