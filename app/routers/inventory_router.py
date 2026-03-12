from fastapi import APIRouter, HTTPException
from ..schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from ..repositories import inventory_repository

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/{food_item_id}", response_model=Inventory)
def get_inventory(food_item_id: int):
    """Get inventory record by food item ID."""
    record = inventory_repository.get_inventory_by_food_id(food_item_id)
    if not record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return record

@router.post("/", response_model=Inventory)
def create_inventory(payload: InventoryCreate):
    """Create a new inventory record."""
    return inventory_repository.create_inventory_record(payload)

@router.patch("/{food_item_id}", response_model=Inventory)
def update_inventory(food_item_id: int, payload: InventoryUpdate):
    """Update an existing inventory record."""
    updated_record = inventory_repository.update_inventory_record(food_item_id, payload)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_record

@router.delete("/{food_item_id}", status_code=204)
def delete_inventory(food_item_id: int):
    """Delete an inventory record."""
    success = inventory_repository.delete_inventory_record(food_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return None