from pathlib import Path
import csv
from decimal import Decimal

DATA_PATH = Path("app/data/food_items.csv")
FIELDNAMES = ["food_item_id", "restaurant_id", "food_name", "price", "description", "course"]

def load_all():
    """load_all() function loads all food items from the CSV file and returns them as a list of dictionaries. If the file doesn't exist, it returns an empty list."""    
    if not DATA_PATH.exists():
        return []
    
    items = []
    with open(DATA_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
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
    """save_all() function takes a list of food item dictionaries and writes them to the CSV file, overwriting any existing data. Ensures the directory exists before writing."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(items)