import uuid
from fastapi import HTTPException
from app.schemas.cartItem import CartItemUpdate, CartItemResponse
from app.repositories.cartItems_repo import load_all, save_all

def update_cartItem(cart_item_id: str, payload: CartItemUpdate) -> CartItemResponse:
    cart_items_data = load_all()
    updated = None
    
    quantity = int(payload["quantity"])
    if quantity <= 0:
        raise ValueError("Quantity cannot be zero or less than")
    
    price_per_item = float(payload["price_per_item"])
    if price_per_item <= 0:
        raise ValueError("Price cannot be zero or less than")
    
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            address_id = it.get("address_id")
            
            updated = CartItemResponse (
                address_id = address_id, 
                cart_item_id = cart_item_id,
                cart_id = it.get("cart_id"), 
                food_item_id = it.get("food_item_id"), 
                quantity = quantity,
                price_per_item = float(price_per_item), 
                subtotal = float(quantity*price_per_item)
                )
            cart_items_data[idx] = updated.model_dump()
            break
        if updated is None:
            raise HTTPException(status_code=404, detail=f"Cart Item '{cart_item_id}' not found")
    save_all(cart_items_data)
    return updated
    

def remove_cartItem(cart_item_id: str) -> None:
    cart_items_data = load_all()
    print([it.get("cart_item_id") for it in cart_items_data])
    found_cart_item = False
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            found_cart_item = True
            cart_items_data.pop(idx)
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")
    save_all(cart_items_data)

