import ulid
from app.schemas.cart_item_schema import CartItemAdd, CartItemResponse
from app.schemas.cart_schema import CartUpdate
from pydantic import ValidationError
from fastapi import HTTPException

def add_cart_item(cartItem: CartItemAdd, price_per_item: float) -> CartItemResponse:
    """Adds a singular cart item and returns a CartItemResponse (cart_item_id, food_item_id, price_per_item, quantity, subtotal)"""
    cart_dict = cartItem.model_dump()
    cart_item_id = str(ulid.new())
    food_item_id = cart_dict["food_item_id"]
    quantity = cart_dict["quantity"]
    subtotal = quantity * price_per_item

    if not quantity: 
        raise ValidationError

    if not price_per_item: 
        raise ValidationError

    return CartItemResponse(
        cart_item_id=cart_item_id, 
        food_item_id=food_item_id, 
        price_per_item=price_per_item, 
        quantity=quantity,
        subtotal=subtotal
    )

def delete_cart_item(cart_current, cart_item_id) -> dict: 
    """Removes the cart_item and returns the cart without this item"""
    found_cart_item = False
    for index, cart in enumerate(cart_current.cart_items):
        if cart.cart_item_id == cart_item_id:
            found_cart_item = True
            cart_current.cart_items.pop(index)
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")
    return cart_current


def update_cart_item(cart_current, cart_item_id, price_of_new_item, cart_update: CartUpdate) -> dict: 
    """Updates the cart item with - food_item, quantity, price and calculates new subtotal"""
    updated_item = cart_update.model_dump()
    found_cart_item = False
    for i, cart in enumerate(cart_current.cart_items): 
        if cart.cart_item_id == cart_item_id:
            found_cart_item = True
            cart.food_item_id = updated_item["food_item_id"]
            cart.quantity = updated_item["quantity"]
            cart.price_per_item = float(price_of_new_item)
            cart.subtotal = float(cart.quantity * cart.price_per_item)
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")
    return cart_current

