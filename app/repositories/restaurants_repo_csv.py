from pathlib import Path
import csv
import os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.csv"

def load_all() -> List[Dict[str, Any]]:
   if not DATA_PATH.exists():
       return []
   with DATA_PATH.open("r", encoding="utf-8") as f:
       reader = csv.DictReader(f)
       return list(reader)

def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["restaurant_id",
    "owner_id",
    "restaurant_name",
    "cuisine",
    "address",
    "open_hour",
    "closed_hour",
    "restaurant_status"
    ]
    
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)