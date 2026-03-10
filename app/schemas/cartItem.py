from pydantic import BaseModel

class CartItemBase(BaseModel):
    food_item_id: str
    quantity: str
    price_per_item: str

class CartItemResponse(CartItemBase): 
    cart_item_id: str
    cart_id: str

class CartItemAdd(BaseModel):
    cart_id: str
    food_item_id: str
    quantity: str 
    price_per_item: str

class CartItemUpdate(BaseModel):
     quantity: str; 
     price_per_item: str