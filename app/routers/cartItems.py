from fastapi import APIRouter, status
from app.schemas.cartItem import CartItemAdd, CartItemResponse
from app.services.cartItems_service import add_cart_item, update_cartItem, remove_cartItem, get_cartItem_by_id

router = APIRouter(prefix="/cart-items", tags=["cartItems"])

@router.get("/by-id/{cart_item_id}", response_model = CartItemResponse)
def get_cart_item_id(cart_item_id: str):
    """Gets a cart item with provided data and returns Cart Item Response data"""
    return get_cartItem_by_id(cart_item_id)

@router.post("/", response_model=CartItemResponse, status_code=201)
def add_cart_item_route(item: CartItemAdd):
    """Creates a cart item with provided data and returns Cart Item Response data"""
    return add_cart_item(item)

@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: str, quantity: int):
    """Updates a cart with the provided data and returns updated cart item"""
    return update_cartItem(cart_item_id, quantity)

@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(cart_item_id: str):
    """Removes a cart item with the provided cart item id. Return is nothing"""
    remove_cartItem(cart_item_id)
    return None

