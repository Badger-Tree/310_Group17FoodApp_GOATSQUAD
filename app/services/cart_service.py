import ulid
from fastapi import HTTPException
from app.schemas.cart_schema import CartCreate, CartResponse
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

    cart_data = load_all_carts()

    cart = {
        "customer_id": customer_id,
        "cart_id": cart_id,
        "cart_items": [],
        "total": 0.0
    }

    cart_data.append(cart)
    
    save_cart(cart_data)
    return cart


def add_to_cart(customer_id, cart_add: CartCreate) -> CartResponse:
    """Adds a new item to the cart if the cart_id associated with the customer exists"""
    cart_dict = cart_add.model_dump()
    food_item_data = load_all_food_items()
    cart_data = load_all_carts()
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
    
    for c in cart_data:
        if c["cart_id"] == cart_response.cart_id:
            c["cart_items"] = cart_response.cart_items
            c["total"] = cart_response.total
            break
    else:
        cart_data.append(cart_response.model_dump())

    save_cart(cart_data)
    return cart_response


def calculateSubtotal(current_cart):
    """Calculates the subtotal of all the current items with the cart_items dictionary"""
    subtotal = 0
    cart_items = getattr(current_cart, "cart_items", None) or current_cart.get("cart_items", [])
    for item in cart_items:
        subtotal += getattr(item, "subtotal", None) or item["subtotal"]
    return subtotal




 