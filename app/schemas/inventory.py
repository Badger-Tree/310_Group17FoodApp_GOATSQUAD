from pydantic import BaseModel, Field
from typing import Optional

class InventoryBase(BaseModel):
    food_item_id: int
    quantity: int = Field(default=0, ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None

class Inventory(InventoryBase):
    inventory_id: int
