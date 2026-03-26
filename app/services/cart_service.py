import ulid
from fastapi import HTTPException
from app.schemas.cart_schema import CartCreate, CartResponse
from app.repositories.food_item_repo import load_all as load_all_food_items
from app.repositories.cart_repo_csv import save_all as save_cart, load_all as load_all_carts
from app.services.cart_item_service import add_cart_item, delete_cart_item, update_cart_item
from app.services.food_item_service import get_food_by_id


def get_cart_by_customer(customer_id: str) -> CartResponse:
    """Gets the cart with the customer_id and returns a CartResponse with information of the cart in question"""
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

"""
THIS WAS TO GET FOOD ITEM ID BUT NOT USED, COULD ALSO CHECK INVENTORY IF THERES TIME
def verify_food_item(food_data): 
    Verifies that the food_item exists
    food_item= get_food_by_id(food_data)
    print(food_item)
    food_item_id = food_item["food_item_id"]
    
    if not food_item_id:    
        raise HTTPException(status_code=404, detail="Food item does not exist")
    return food_item
"""

def add_to_cart(customer_id, cart_add: CartCreate) -> CartResponse:
    """Adds a new item to the cart if the cart_id associated with the customer exists"""
    food_data = cart_add.model_dump()
    cart_data = load_all_carts()

    food_item = get_food_by_id(food_data["food_item_id"])
    if not food_item: 
        raise HTTPException(status_code=404, detail="Food item does not exist")
    price_per_item = food_item["price"]
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
    """Calculates the subtotal of all the current items with the cart_items"""
    subtotal = 0
    cart_items = getattr(current_cart, "cart_items", [])
    for item in cart_items:
        subtotal += getattr(item, "subtotal", None) or item["subtotal"]
    return subtotal


def delete_from_cart(customer_id, cart_item_id) -> CartResponse:
    """Deletes a cart item with the provided customer id and cart item id"""
    cart_data = load_all_carts()
    cart_current = get_cart_by_customer(customer_id) 
    cart_after_delete = delete_cart_item(cart_current, cart_item_id) 
    cart_total= calculateSubtotal(cart_after_delete)
    
    for c in cart_data:
        if c["cart_id"] == cart_after_delete.cart_id:
            c["cart_items"] = cart_after_delete.cart_items
            c["total"] = cart_total
            break
    else:
        cart_data.append(c)

    save_cart(cart_data)
    return c

 
def update_cart(customer_id, cart_item_id, cart_update) -> CartResponse:
    """Updates a cart item with the newly updates values"""
    cart_data = load_all_carts()
    food_data = cart_update.model_dump()
    food_item = get_food_by_id(food_data["food_item_id"])
    if not food_item: 
        raise HTTPException(status_code=404, detail="Food item does not exist")
    price_of_updated_item = food_item["price"]

    cart_current = get_cart_by_customer(customer_id) 
    cart_after_update = update_cart_item(cart_current, cart_item_id, price_of_updated_item, cart_update) 
    cart_total= calculateSubtotal(cart_after_update)
    
    for c in cart_data:
        if c["cart_id"] == cart_after_update.cart_id:
            c["cart_items"] = cart_after_update.cart_items
            c["total"] = cart_total
            break
    else:
        cart_data.append(c)

    save_cart(cart_data)
    return c

def clear_cart(customer_id, cart_id): 
    """Clears the cart completely"""
    cart_data = load_all_carts() 

    found_cart_item = False
    for index, cart in enumerate(cart_data):  
        if cart["cart_id"] == cart_id:
            found_cart_item = True  
            cart["customer_id"] == customer_id           
            cart["cart_items"] = []        
            cart["total"] = 0.0           
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found")
    save_cart(cart_data)

    return cart