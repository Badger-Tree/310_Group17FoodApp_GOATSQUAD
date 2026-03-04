from pydantic import BaseModel
from app.schemas.cartItem import CartItemResponse
from typing import List
from typing import Optional
   

class CartBase(BaseModel):
    cart_id: str
    customer_id: str

class CartResponse(BaseModel): 
    items: Optional[List[CartItemResponse]] = None
    subtotal: Optional[float] = None

class CartCreate(CartBase): 
    pass