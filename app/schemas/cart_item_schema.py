from pydantic import BaseModel, PositiveFloat, PositiveInt

class CartItemBase(BaseModel):
    cart_item_id: str
    food_item_id: int
    quantity: PositiveInt
    price_per_item: PositiveFloat
    subtotal: PositiveFloat

class CartItemResponse(CartItemBase): 
    pass

class CartItemAdd(BaseModel):
    food_item_id: int
    quantity: PositiveInt
