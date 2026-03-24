import ulid
from app.schemas.cart_item_schema import CartItemAdd, CartItemResponse
from pydantic import ValidationError

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
