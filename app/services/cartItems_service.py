import uuid
from fastapi import HTTPException
from app.schemas.cartItem import CartItemAdd, CartItemResponse
from app.repositories.cartItems_repo_csv import load_all, save_all
from app.services.cart_services import create_cart
from app.services.food_item_service import get_food_by_id
from app.services.address_service import get_address_by_customer_id_service
from app.services.session_manager_service import get_user_from_session
from app.services.user_service import get_user_by_id_service
from app.schemas.Token import Token

def load_all_data(): 
    cart_items = load_all()
    return cart_items

def load_cart_item_id(cart_item_id: str): 
    cart_items = load_all_data()
    found_cart_item = False
    for c in cart_items: 
        if c["cart_item_id"] == cart_item_id: 
            found_cart_item = True
            return c
    if not found_cart_item:
        raise_exception_404(cart_item_id)

def raise_exception_404(cart_item_id): 
    raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")

def raise_exception_400(): 
    raise HTTPException(status_code=400, detail="cart_item_id cannot be empty")


def get_cartItem_by_id(cart_item_id: str) -> CartItemResponse:
    """Gets a cart item by its id and returns a CartItemResponse"""
    cart_item_id = str(cart_item_id).strip()
    if not cart_item_id: 
        raise_exception_400()
    cart_item = load_cart_item_id(cart_item_id)
    return CartItemResponse(**cart_item)
    

def add_cart_item(item):
    """Adds an item to a cart and returns information of a new cart item"""
    if isinstance(item, dict):
        item = CartItemAdd(**item)
    cart_items_data = load_all()

    foodItem = get_food_by_id(item.food_item_id)
    food_item_id = foodItem.get("food_item_id")
    if food_item_id is None:
        raise HTTPException(status_code=404, detail=f"Food id'{food_item_id}' not found")

    customer = get_user_from_session(Token(token = "cdf4f8431bf25e4a868e4d56041fa2dd"))
    customer_id = customer.id
    print(customer_id)

    address_id = None
    addressItem = get_address_by_customer_id_service(customer_id)
    if addressItem:
     address_id = addressItem[0].address_id

    price_per_item = float(foodItem.get("price"))
    quantity = item.quantity

    cart_exists = False
    for c in cart_items_data: 
        if str(c.get("customer_id")) == str(customer_id):             
            cart_exists = True
            cart_id = c.get("cart_id")
            break

    if not cart_exists: 
        cart_id = str(uuid.uuid4())
        create_cart(cart_id, customer_id)  

    subtotal = quantity * price_per_item

    new_cart_item = {                                     
        "cart_item_id": str(uuid.uuid4()),                 
        "cart_id": cart_id,
        "customer_id": customer_id,
        "address_id": address_id, 
        "food_item_id": food_item_id,
        "quantity": quantity,
        "price_per_item": price_per_item,
        "subtotal": subtotal
    }

    cart_items_data.append(new_cart_item)
    save_all(cart_items_data)
    return CartItemResponse(**new_cart_item)


def update_cartItem(cart_item_id: str, quantity: int) -> CartItemResponse:
    """Updates a cart item and returns a CartItemResponse"""
    cart_items_data = load_all()
    updated = None

    quantity = int(quantity)
    if quantity <= 0: 
        raise ValueError("Quantity cannot be negative")
    
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            address_id = it.get("address_id")
            price_per_item = float(it.get("price_per_item", 0))
            subtotal = float(quantity*price_per_item)
            
            updated = CartItemResponse (
                address_id = address_id, 
                cart_item_id = cart_item_id,
                cart_id = it.get("cart_id"), 
                food_item_id = it.get("food_item_id"), 
                quantity = quantity,
                price_per_item = float(price_per_item), 
                subtotal = float(subtotal)
                )
            cart_items_data[idx] = updated.model_dump()
            break
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Cart Item '{cart_item_id}' not found")
    save_all(cart_items_data)
    return updated
    

def remove_cartItem(cart_item_id: str) -> None:
    """Removes a cart item"""
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

