from pathlib import Path
import csv
from pydantic_core import to_jsonable_python
import json

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cart.csv"

def load_all() -> list[dict]:
    """Loads all cart data from the csv file and converts the fields as well as the cart_items to dictionary format"""
    if not DATA_PATH.exists():
        return []

    carts = []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader: 
            items = row.get("cart_items", "")
            try:
                cart_items = json.loads(items) if items else []
            except json.JSONDecodeError:
                    cart_items = []
            
            carts.append({
                "cart_id": str(row["cart_id"]), 
                "customer_id": str(row["customer_id"]), 
                "cart_items": cart_items, 
                "total": float(row["total"]) if row.get("total") else 0.0
            })
        return carts
   
def save_all(carts):
    """Saves all cart data to a csv file cart.csv"""
    with DATA_PATH.open("w", newline="", encoding="utf-8") as f:
        fields = ["customer_id", "cart_id", "cart_items", "total"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        if not isinstance(carts, list):
            raise ValueError("Data should be a list")
                
        for cart in carts:
            writer.writerow({
                "customer_id": cart["customer_id"],
                "cart_id": cart.get("cart_id"),
                "cart_items": json.dumps([c.model_dump() if hasattr(c, "model_dump") else c for c in cart["cart_items"]]),
                "total": cart.get("total", 0)
            })

