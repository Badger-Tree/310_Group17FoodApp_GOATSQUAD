from pathlib import Path
import json, os
from typing import List, Dict, Any
from decimal import Decimal

#finds data folder
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_items.json"

#handles dec math saving to json
class DecimalEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)
    
def load_all() -> List[Dict[str, Any]]:
    #checking if file exists; if not, return empty list
    if not DATA_PATH.exists():
        return []
    
    #open file, turn json text into list
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_all(food_items: List[Dict[str, Any]]) -> None:
    #makes sure data dir exists before saving 
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    #prevent data corruption by making temp file
    temp = DATA_PATH.with_suffix(".temp")

    with temp.open("w", encoding="utf-8") as f:
        #cls=DecimalEncode to handle price field
        json.dump(food_items, f, ensure_ascii=False, indent=2, cls=DecimalEncode)

    #replace old file with new
    os.replace(temp, DATA_PATH)