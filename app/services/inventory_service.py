from typing import Optional
from app.repositories.inventory_repository import load_all, save_all
from app.schemas.inventory import Inventory, InventoryCreate

def create_inventory_record(payload: InventoryCreate) -> Inventory:
    """Create new inventory record with auto-incremented inventory_id"""
    items = load_all()
    new_id = max((int(item["inventory_id"]) for item in items), default=0) + 1
    new_record = {
        "inventory_id": new_id,
        "food_item_id": payload.food_item_id,
        "quantity": payload.quantity
    }
    items.append(new_record)
    save_all(items)
    return Inventory(**new_record)

def get_inventory_by_food_id(food_item_id: int) -> Optional[Inventory]:
    """Finds an inventory record specifically by the food_item_id"""
    items = load_all()
    for item in items:
        if int(item["food_item_id"]) == food_item_id:
            return Inventory(**item)
    return None

def delete_inventory_record(food_item_id: int) -> bool:
    """Delete an inventory record by food_item_id"""
    items = load_all()
    new_items = [item for item in items if int(item["food_item_id"]) != food_item_id]

    if len(new_items) == len(items):
        return False  

    save_all(new_items)
    return True

def check_availability(food_item_id: int, quantity: int) -> bool:
    """Check if the requested quantity of a food item is available in inventory."""
    record = get_inventory_by_food_id(food_item_id)
    if not record:
        return False

    return record.quantity >= quantity

def update_inventory(food_item_id: int, new_quantity: int) -> Inventory:
    """Update the quantity of a specific food item in inventory."""
    if new_quantity < 0:
        raise ValueError("Quantity cannot be negative")
    
    items = load_all()
    for item in items:
        if int(item["food_item_id"]) == food_item_id:
            item["quantity"] = new_quantity
            save_all(items)
            return Inventory(**item)
    return None