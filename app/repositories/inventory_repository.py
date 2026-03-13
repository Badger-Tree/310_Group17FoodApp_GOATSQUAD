import csv
from pathlib import Path
from typing import List, Optional
from app.schemas.inventory import Inventory, InventoryCreate, InventoryUpdate

DATA_PATH = Path("app/data/inventory.csv")

def load_all() -> List[dict]:
    """Load all inventory items from the CSV file as a list of dictionaries"""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, mode='r', newline='') as file:
        return list(csv.DictReader(file))
    
def save_all(items: List[dict]):
    """Write the list of inventory items back to the CSV file"""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    headers = ["inventory_id", "food_item_id", "quantity"]
    with open(DATA_PATH, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(items)

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

def update_inventory(food_item_id: int, payload: InventoryUpdate) -> Optional[Inventory]:
    """Update the quantity for a specific food item"""
    items = load_all()
    updated_item = None

    for item in items:
        if int(item["food_item_id"]) == food_item_id:
            if payload.quantity is not None:
                item["quantity"] = payload.quantity

            updated_item = item
            break

    if updated_item:
        save_all(items)
        return Inventory(**updated_item)

    return None

def delete_inventory_record(food_item_id: int) -> bool:
    """Delete an inventory record by food_item_id"""
    items = load_all()
    new_items = [item for item in items if int(item["food_item_id"]) != food_item_id]

    if len(new_items) == len(items):
        return False  

    save_all(new_items)
    return True