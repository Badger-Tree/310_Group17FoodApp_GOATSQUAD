from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.csv"

def load_all() -> List[Dict[str, Any]]:
   if not DATA_PATH.exists():
       return []
   
def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["id",
                "email",
                "first_name",
                "last_name",
                "password",
                "role",
                "created_date"]
                
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)