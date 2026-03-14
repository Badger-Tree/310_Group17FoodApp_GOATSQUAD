from pathlib import Path
import json, os
from typing import List, Dict, Any
from decimal import Decimal 

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cartItems.json"

def load_all() -> List[Dict[str, Any]]:
   if not DATA_PATH.exists():
       return []
   with DATA_PATH.open("r", encoding="utf-8") as f:
       return json.load(f)

def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")

    def decimal_converter(obj):
        if isinstance(obj, Decimal):
            return float(obj)  
        raise TypeError("decimal is not JSON serializable")
    
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, default=decimal_converter)
    os.replace(tmp, DATA_PATH)