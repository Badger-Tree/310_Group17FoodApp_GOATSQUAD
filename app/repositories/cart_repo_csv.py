from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cart.csv"

def load_all() -> List[Dict[str, Any]]:
   """load_all() function loads all carts from the CSV file and returns them as a list of dictionaries. If the file doesn't exist, it returns an empty list."""
   if not DATA_PATH.exists():
       return []
   with DATA_PATH.open("r", encoding="utf-8") as f:
       reader = csv.DictReader(f)
       return list(reader)
   
def save_all(items: List[Dict[str, Any]]) -> None:
    """save_all() function takes a list of cartItem dictionaries and writes them to the CSV file"""
    if not isinstance(items, list):
        raise ValueError("Data needs to be a list")
    
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = [
    "cart_id",
    "customer_id"
    ]
    
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)