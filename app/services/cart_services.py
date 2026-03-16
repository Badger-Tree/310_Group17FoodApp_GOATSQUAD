from typing import List, Dict
from fastapi import HTTPException
from app.schemas.cart import CartResponse, CartBase
from app.repositories.cart_repo_csv import load_all, save_all
from app.repositories.cartItems_repo_csv import load_all as load_all_cart_items
import csv
from pathlib import Path

def list_carts() -> List[CartResponse]:
     """Returns all carts in the cart data"""
     return load_all

def load_all() -> list[dict]:
    """Loads data from cart.csv and returns it as a list of dictionaries."""
    file_path = Path("app/data/cart.csv")
    with file_path.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)  
        return [{x.strip(): y.strip() for x, y in row.items()} for row in reader]

def get_cart_by_id_service(cart_id: str) -> CartBase:
    """Gets a cart by its id and returns a CartBase: (cart_id, customer_id)"""
    if not cart_id:
        raise HTTPException(status_code=400, detail="cart_id cannot be empty")

    cart_data = load_all()

    for item in cart_data:
        if item.get("cart_id") == cart_id:
            return CartBase(
                cart_id=item.get("cart_id"),
                customer_id=item.get("customer_id")
            )
    raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found")

def get_items_by_cart(cart_id: str) -> dict:
    """Gets a cart by its id and returns all items in the cart as a dictionary"""
    cart_items_data = load_all_cart_items()
    cart_id = str(cart_id).strip()
    if not cart_id: 
        raise HTTPException(status_code=400, detail="cart_id cannot be empty")
   
    cart_items_responses = []
    calculateSubtotal = 0.0
    
    for it in cart_items_data:
        if it.get("cart_id") == cart_id:
            cart_items_responses.append({
                "address_id": it.get("address_id"),
                "cart_item_id": it.get("cart_item_id"),
                "cart_id": str(it.get("cart_id")),
                "food_item_id": int(it.get("food_item_id")),
                "quantity": int(it.get("quantity")),
                "price_per_item": float(it.get("price_per_item")),
                "subtotal": float(it.get("subtotal"))
            })
            calculateSubtotal += float(it.get("subtotal"))

    if not cart_items_responses:
        raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found")
    
    return { 
        "cartList": cart_items_responses,
        "total": calculateSubtotal
    }

def create_cart(cart_id: str, customer_id: str):
    """Creates a cart with cart_id and customer_id if the cart does not exist"""
    cart_data = load_all()
    cart_id = cart_id.strip()
    customer_id = customer_id.strip()

    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id cannot be empty")
    
    new_cart = {
        "cart_id": cart_id,
        "customer_id": customer_id
    }
   
    cart_data.append(new_cart)
    save_all(cart_data)
    return new_cart

"""
def clear_cart(cart_id: str): 
    clear_items = get_items_by_cart(cart_id)
"""
