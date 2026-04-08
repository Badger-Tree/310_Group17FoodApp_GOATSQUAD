import csv, os
from pathlib import Path
from typing import List, Dict, Any

DATA_PATH = Path("app/data/inventory.csv")

def load_all() -> List[dict]:
    """Load all inventory items from the CSV file as a list of dictionaries"""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, mode='r', newline='') as file:
        return list(csv.DictReader(file))
    
def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["inventory_id", "food_item_id", "quantity"]
                
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)

def find_by_food_id_repo(food_item_id: int) -> dict | None:
    """search csv for specific food item id and return raw dictionary"""
    items = load_all()
    for item in items:
        if int(item["food_item_id"]) == food_item_id:
            return item
    return None
