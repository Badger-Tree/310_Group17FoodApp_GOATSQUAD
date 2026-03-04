import uuid
from fastapi import HTTPException
from app.schemas.cartItem import CartItemResponse, CartItemUpdate
from app.repositories.cartItems_repo import load_all, save_all
from typing import List
from app.services.cart_services import create_cart

#gets the cartItem by its id
def get_cartItem_by_id(cart_item_id: str) -> CartItemResponse:
    cart_items_data = load_all()
    for it in cart_items_data:
        #checks if the cart_item_id provided exists in the cart_item_data
        if it.get("cart_item_id") == cart_item_id:
            #returns CartItemResponse if true
            return CartItemResponse(**it)
    raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")

#gets the items by their cart id
def get_items_by_cart(cart_id: str) -> List[CartItemResponse]:
    cart_items_data = load_all()
    #creates an empty cart_item_response_array
    cart_items_responses = []
    subtotal = 0
    
    for it in cart_items_data:
        if it.get("cart_id") == cart_id:
            #if the cart_id provided exists add the cart to the response array
            #add together subtotal for the same cart_id
            cart_item_id = it.get("cart_item_id")
            food_item_id = it.get("food_item_id")
            quantity = it.get("quantity")
            price_per_item = float(it.get("price_per_item"))
            subtotal += float(quantity * price_per_item)
            cart_items_responses.append({
                "cart_item_id": cart_item_id,
                "cart_id": cart_id,
                "food_item_id": food_item_id,
                "quantity": quantity,
                "price_per_item": price_per_item,
                "subtotal": subtotal
            })
    if not cart_items_responses:
        raise HTTPException(status_code=404, detail=f"Cart'{cart_id}' not found")
    #returns the cart_item_response array
    return cart_items_responses


def add_cart_item(item):
    #loads data from other classes, this will change once I pull others code
    cart_items_data = load_all()

    #checks if a cart exists for the customer in question
    cart_exists = False
    for c in cart_items_data: 
        if str(c.get("customer_id")) == item.customer_id:             
            cart_exists = True
            #save the cart_id for this particular customer
            cart_d = c.get("cart_id")
            cart_id = cart_d
            customer_id = item.customer_id
            break

    #if cart does not exist for this customer, we want to create their cart for the first item
    if not cart_exists: 
        cart_id = str(uuid.uuid4())
        #Now we assign the customer_id of this cart to the current customer
        customer_id = item.customer_id
        #We let the cart class create this new cart because it is the first 
        create_cart(cart_id, customer_id)    
    
    #DOUBLE CHECK QUANTITY AMOUNTS ONCE EVERYTHING COMES TOGETHER
    quantity = item.quantity
    price_per_item = float(item.price_per_item)
    subtotal = quantity * price_per_item
    food_item_id = item.food_item_id

    #creates cart_item
    #even if first cart just got created this will work
    new_cart_item = {                                     
        "cart_item_id": str(uuid.uuid4()),                 
        "cart_id": cart_id,
        "customer_id": customer_id,
        "food_item_id": food_item_id,
        "quantity": quantity,
        "price_per_item": price_per_item,
        "subtotal": subtotal
    }

    #Now cart_items_data contains this cart with the cart item
    cart_items_data.append(new_cart_item)
    save_all(cart_items_data)
    return CartItemResponse(**new_cart_item)



def update_cartItem(cart_item_id: str, payload: CartItemUpdate) -> CartItemResponse:
    cart_items_data = load_all()
    #Search through cart_items_data and see if anything equals to the cart_item_id provided
    for idx, it in enumerate(cart_items_data):
        if it.get("cart_item_id") == cart_item_id:
            quantity = int(payload.quantity) 
            price_per_item = float(payload.price_per_item)
            subtotal = float(quantity * price_per_item)
            #if the id exists then update all required fields with the proper information 
            updated = CartItemResponse( 
                cart_id = it.get("cart_id"),
                cart_item_id = it.get("cart_item_id"),
                food_item_id = it.get("food_item_id"),
                quantity = int(payload.quantity), 
                price_per_item = float(payload.price_per_item),
                subtotal = float(subtotal)
            )
            data = updated.dict()
            cart_items_data[idx] = data
            save_all(cart_items_data)
            return updated
    raise HTTPException(status_code=404, detail=f"Cart Item '{cart_item_id}' not found")
   
    

def remove_cartItem(cart_item_id: str) -> None:
    cart_items_data = load_all()
    found_cart_item = False
    for i, cart in enumerate(cart_items_data):
        if cart.get("cart_item_id") == cart_item_id:
            found_cart_item = True
            #This removes the cart_item that is to be removed
            cart_items_data.pop(i)
            break
    if not found_cart_item:
        raise HTTPException(status_code=404, detail=f"Item '{cart_item_id}' not found")
    save_all(cart_items_data)



    
