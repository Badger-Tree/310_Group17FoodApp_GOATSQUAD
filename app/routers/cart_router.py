from fastapi import APIRouter, Header
from app.schemas.cart_schema import CartCreate, CartResponse, CartUpdate
from app.services.cart_service import add_to_cart, delete_from_cart, update_cart
from app.services.cart_service import add_to_cart, delete_from_cart, clear_cart
from app.schemas.Token import Token
from app.services.session_manager_service import get_user_from_session
from fastapi import HTTPException

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/food_item/add", response_model = CartResponse, status_code=201)
def add_item(cart_item: CartCreate, token: str = Header(...)):
        """Takes a CartCreate object containing food_item_id and quantity as well as a Token and adds an item to the cart"""
        session = Token(token=token)
        current_customer = get_user_from_session(session)
        print(f"Using user id: {current_customer.id}")
        customer_id = current_customer.id
        if not customer_id: 
                raise HTTPException(status_code=404, detail=f"Customer'{customer_id}' not found")
        return add_to_cart(customer_id, cart_item)


@router.delete("/food_item/remove", status_code=201)
def remove_cart_item(cart_item_id: str, token: str = Header(...)):
    """Removes a cart item with the provided cart item id and current customer token"""
    session = Token(token=token)
    current_customer = get_user_from_session(session)
    customer_id = current_customer.id
    if not customer_id: 
        raise HTTPException(status_code=404, detail=f"Customer'{customer_id}' not found")
    return delete_from_cart(customer_id, cart_item_id)


@router.put("/food_item/update", status_code=201)
def update_cart_item(cart_item_id: str, cart_update: CartUpdate, token: str = Header(...)):
    """Updates a cart item with the provided cart item id and current customer token"""
    session = Token(token=token)
    current_customer = get_user_from_session(session)
    customer_id = current_customer.id
    if not customer_id: 
        raise HTTPException(status_code=404, detail=f"Customer'{customer_id}' not found")
    return update_cart(customer_id, cart_item_id, cart_update)

    
