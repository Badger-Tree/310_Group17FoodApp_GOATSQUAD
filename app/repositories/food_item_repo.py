from pathlib import Path
import csv
from decimal import Decimal

#finds data folder
DATA_PATH = Path("app/data/food_items.csv")
FIELDNAMES = ["food_item_id", "restaurant_id", "food_name", "price", "description", "course"]
    
def load_all():
    #checking if file exists; if not, return empty list
    if not DATA_PATH.exists():
        return []
    
    items = []
    with open(DATA_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            #manual type conversion since csv is all in str
            items.append({
                "food_item_id": int(row["food_item_id"]),
                "food_name": row["food_name"],
                "restaurant_id": int(row["restaurant_id"]),
                "price": Decimal(row["price"]),
                "description": row["description"],
                "course": row["course"]
            })
    return items
    
def save_all(items):
    #makes sure data dir exists before saving 
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(items)