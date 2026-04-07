from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "track_food_items.csv"

def load_all() -> List[Dict[str, Any]]:
    """load all() function loads items from CSV and convert fields to int"""
    if not DATA_PATH.exists():
        return []
    
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    for item in items:
        if "food_item_id" in item:
            item["food_item_id"] = int(item["food_item_id"])
        if "order_count" in item:
            item["order_count"] = int(item["order_count"])
    
    return items
   
def save_all(items: List[Dict[str, Any]]) -> None:
    """save_all() function takes a list of item dictionaries and writes them to the CSV file"""
    tmp = DATA_PATH.with_suffix(".tmp")

    fields = ["food_item_id", "order_count"]
    
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)