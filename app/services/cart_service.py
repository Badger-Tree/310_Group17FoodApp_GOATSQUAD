import ulid
from typing import Dict, Any
from fastapi import HTTPException
from app.schemas.Token import Token
from app.schemas.cart_schema import CartCreate, CartResponse, CartBase
from app.repositories.food_item_repo import load_all as load_all_food_items
from app.repositories.cart_repo_csv import save_all as save_cart, load_all as load_all_carts
from app.services.cart_item_service import add_cart_item


def get_cart_by_customer(customer_id: str) -> CartResponse:
    """Gets the cart but the customer_id and returns a CartResponse with information of the cart in question"""
    cart_data = load_all_carts()
    for c in cart_data:
        if c.get("customer_id") == str(customer_id):
            return CartResponse(**c)
    raise HTTPException(status_code=404, detail=f"Customer'{customer_id}' cart not found")

def create_cart(current_customer: str): 
    """Creates a cart for a new customer"""
    customer_id = str(current_customer)
    cart_id = str(ulid.new())

    cart = {
        "customer_id": customer_id,
        "cart_id": cart_id,
        "cart_items": [],
        "total": 0.0
    }
    
    save_cart(cart)
    return cart


def add_to_cart(customer_id, cart_add: CartCreate) -> CartResponse: 
    """Adds a new item to the cart if the cart_id associated with the customer exists"""
    cart_dict = cart_add.model_dump()
    food_item_data = load_all_food_items()
    food_item_id = cart_dict["food_item_id"]
    food_item_obj = next(
        (f for f in food_item_data if f["food_item_id"] == food_item_id), None  
    )
    if not food_item_obj:    
        raise HTTPException(status_code=404, detail="Food item does not exist")
    price_per_item = food_item_obj["price"]

    cart_item = add_cart_item(cart_add, price_per_item) 
    cart_current = get_cart_by_customer(customer_id) 
    if not cart_current.cart_items: 
        cart_current.cart_items = []

    cart_current.cart_items.append(cart_item) 
    total = calculateSubtotal(cart_current)

    cart_response = CartResponse(
        customer_id=cart_current.customer_id,
        cart_id=cart_current.cart_id,
        cart_items= cart_current.cart_items, 
        total = total
    )  
    final_cart = cart_append(load_all_carts(), cart_response)
    save_cart(final_cart)
    return cart_response


def cart_append(all_carts, cart_response): 
    """Takes current list of carts in the dataset, only making the change to the cart_id that matches the cart_response"""
    updated_carts = []
    for c in all_carts:
        if c["cart_id"] == cart_response.cart_id:
            merged_cart_items = c["cart_items"] + cart_response.cart_items
            c["cart_items"] = merged_cart_items
            c["total"] = calculateSubtotal(c)
            updated_carts.append(c)
    return updated_carts
    

def calculateSubtotal(current_cart):
    """Calculates the subtotal of all the current items with the cart_items dictionary"""
    subtotal = 0
    cart_items = getattr(current_cart, "cart_items", None) or current_cart.get("cart_items", [])
    for item in cart_items:
        subtotal += getattr(item, "subtotal", None) or item["subtotal"]
    return subtotal




 