from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cartItems.csv"

def load_all() -> List[Dict[str, Any]]:
    """load all() function loads items from CSV and convert fields to int"""
    if not DATA_PATH.exists():
        return []
    
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        items = list(reader)
    
    for item in items:
        if "restaurant_name" in item:
            item["restaurant_name"] = str(item["restaurant_name"])
        if "order_count" in item:
            item["order_count"] = int(item["order_count"])
    
    return items
   
def save_all(items: List[Dict[str, Any]]) -> None:
    """save_all() function takes a list of item dictionaries and writes them to the CSV file"""
    if not isinstance(items, list):
        raise ValueError("Data should be a list")
    
    tmp = DATA_PATH.with_suffix(".tmp")

    fields = [                                     
    "restaurant_name",   
    "order_count"              
    ]
    
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)