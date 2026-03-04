from typing import List
from app.schemas.carts import CartResponse
from app.repositories.cart_repo import load_all
from app.repositories.cart_repo import save_all
from fastapi import HTTPException 

def list_carts() -> List[CartResponse]:
    return [CartResponse(**it) for it in load_all()]

def get_cart_by_id_service(cart_id : str) -> CartResponse:
    from app.repositories.cartItems_repo import load_all as load_all_cart_items
    cart_data = load_all()
    item_data = load_all_cart_items()
    cart_response = []
    for it in cart_data:
        #checks if the cart provided exists in the cart_data
        if it.get("cart_id") == cart_id:
            item = None
            subtotal = 0
            for item in item_data:
                if str(item.get("cart_id")) == cart_id:
                    cart_response.append(item)
                    subtotal += item.get("quantity") * item.get("price_per_item")

            #returns CartResponse if true
            return CartResponse(
               items = cart_response,
               subtotal = subtotal
            )
    raise HTTPException(status_code=404, detail=f"Item '{cart_id}' not found")

#This is to create a cart for a customer's very first item
def create_cart(cart_id: str, customer_id: str):
    cart_data = load_all()

    #creates a new cart information 
    new_cart = {
        "cart_id": cart_id,
        "customer_id": customer_id
    }
    #adds this cart to the cart data set 
    cart_data.append(new_cart)
    save_all(cart_data)
    return new_cart

    
"""
def saveCart(cart_id : str) -> OrderResponse:
    from app.services.cartItems_repo import load_all as load_all_items
    from app.services.cartItems_service import get_items_by_cart
    
    cart_item_data = load_all_items

    item = None
    for i in cart_item_data: 
        if i.get("cart_id") == cart_id:
            item = i
            break
    else raise and exception
    if cart is None:
        raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found")
   
   subtotal = 0
   get the items of a specific cart in cartItems data
   items = get_items_by_cart(cart_id)
   for cartItem in items:
        subtotal += item.quantity * item.price_per_item
        return CartResponse(
        cart_id=cart["cart_id"],
        customer_id=cart["customer_id"],
        subtotal = subtotal
    )
"""
