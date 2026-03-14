import uuid
from fastapi import HTTPException
from app.schemas.cartItem import CartItemAdd, CartItemResponse
from app.repositories.cartItems_repo import load_all, save_all
from app.services.cart_services import create_cart
from app.services.food_item_service import get_food_by_id
from app.services.address_service import get_address_by_customer_id_service


def get_cartItem_by_id(cart_item_id: str) -> CartItemResponse:
    """This gets a cart item by its id and returns a CartItemResponse: (food_item_id,
        quantity, price_per_item, cart_item_id, cart_id, subtotal"""
    cart_items_data = load_all()
    cart_item_id = str(cart_item_id).strip()
    if not cart_item_id:
        raise HTTPException(status_code=400, detail="cart_item_id cannot be empty")
    for it in cart_items_data:
        if it.get("cart_item_id") == cart_item_id:
            return CartItemResponse(**it).model_dump()
    raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")

def add_cart_item(item):
    """Adds an item to a cart and returns information of a new cart item"""
    if isinstance(item, dict):
        item = CartItemAdd(**item)

    cart_items_data = load_all()
    customer_id = item.customer_id
    quantity = item.quantity

    getFoodItem= item.food_item_id
    foodItem= get_food_by_id(getFoodItem)
    food_item_id = foodItem.get("food_item_id")
   
    price_per_item = float(foodItem.get("price"))

    addressItem = get_address_by_customer_id_service(customer_id)
    if addressItem:
     address_id = addressItem[0].address_id

    cart_exists = False
    for c in cart_items_data: 
        if str(c.get("customer_id")) == item.customer_id:             
            cart_exists = True
            cart_id = c.get("cart_id")
            customer_id = item.customer_id
            break

    if not cart_exists: 
        cart_id = str(uuid.uuid4())
        customer_id = item.customer_id
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




