from fastapi import APIRouter
from app.schemas.cartItem import CartItemResponse
from app.services.cartItems_service import get_cartItem_by_id

router = APIRouter(prefix="/cart-items", tags=["cartItems"])

@router.get("/by-id/{cart_item_id}", response_model = CartItemResponse)
def get_cart_item_id(cart_item_id: str):
        return get_cartItem_by_id(cart_item_id)

