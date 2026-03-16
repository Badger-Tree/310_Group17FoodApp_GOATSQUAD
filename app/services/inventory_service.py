from app.repositories import inventory_repository
from app.schemas.inventory import Inventory, InventoryUpdate, InventoryCreate

def get_item(food_item_id: int):
    """Get inventory record by food item ID."""
    return inventory_repository.get_inventory_by_food_id(food_item_id)

def create_item(payload: InventoryCreate):
    """Create a new inventory record."""
    return inventory_repository.create_inventory_record(payload)

def remove_item(food_item_id: int):
    """Delete an inventory record."""
    return inventory_repository.delete_inventory_record(food_item_id)

def check_availability(food_item_id: int, quantity: int) -> bool:
    """Check if the requested quantity of a food item is available in inventory."""
    record = inventory_repository.get_inventory_by_food_id(food_item_id)
    if not record:
        return False

    return record.quantity >= quantity

def update_stock(food_item_id: int, new_quantity: int) -> Inventory:
    """Update the quantity of a specific food item in inventory."""
    if new_quantity < 0:
        raise ValueError("Quantity cannot be negative")
    
    payload = InventoryUpdate(quantity=new_quantity)
    updated_record = inventory_repository.update_inventory(food_item_id, payload)
    return updated_record