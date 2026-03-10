from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "deliveries.csv"

def load_all() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["order_id", "courier_id", "created_date", "address_id", "delivery_status", "delivery_id"]
    
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items) 

    os.replace(tmp, DATA_PATH)

    