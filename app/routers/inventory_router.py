from fastapi import APIRouter, HTTPException
from ..schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from ..services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/{food_item_id}", response_model=Inventory)
def get_inventory(food_item_id: int):
    """Get inventory record by food item ID."""
    record = inventory_service.get_item(food_item_id)
    if not record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return record

@router.post("/", response_model=Inventory)
def create_inventory(payload: InventoryCreate):
    """Create a new inventory record."""
    return inventory_service.create_item(payload)

@router.patch("/{food_item_id}", response_model=Inventory)
def update_inventory(food_item_id: int, payload: InventoryUpdate):
    """Update an existing inventory record."""
    updated_record = inventory_service.update_stock(food_item_id, payload.quantity)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_record

@router.delete("/{food_item_id}", status_code=204)
def delete_inventory(food_item_id: int):
    """Delete an inventory record."""
    success = inventory_service.remove_item(food_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return None