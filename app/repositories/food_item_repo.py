from pathlib import Path
import csv, os
from typing import List, Dict, Any
from decimal import Decimal

DATA_PATH = Path("app/data/food_items.csv")

def load_all():
    """load_all() function loads all food items from the CSV file and returns them as a list of dictionaries. If the file doesn't exist, it returns an empty list."""    
    if not DATA_PATH.exists():
        return []
    
    items = []
    with open(DATA_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({
                "food_item_id": int(row["food_item_id"]),
                "food_name": row["food_name"],
                "restaurant_id": int(row["restaurant_id"]),
                "price": Decimal(row["price"]),
                "description": row["description"],
                "course": row["course"]
            })
    return items

def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["food_item_id", "restaurant_id", "food_name", "price", "description", "course"]
    
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)