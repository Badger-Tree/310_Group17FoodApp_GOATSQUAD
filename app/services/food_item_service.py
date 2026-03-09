from ..schemas.food_item import FoodItemCreate, FoodItemUpdate
from ..repositories.food_item_repo import load_all, save_all

def list_food_items():
    """list_food_items() retrieves all food items and returns as a list of dictionaries."""
    return load_all()

def create_food_item(payload: FoodItemCreate):
    """create_food_item() takes a FoodItemCreate object, generates a new unique ID, saves it to the CSV file, and returns the created item as a dictionary."""
    items = load_all()

    new_id = max([item["food_item_id"] for item in items], default=0) + 1

    new_food = payload.model_dump()
    new_food["food_item_id"] = new_id

    items.append(new_food)
    save_all(items)
    return new_food

def get_food_by_id(food_id: int):
    """get_food_by_id() retrieves a single food item by ID and returns it as a dictionary; if not found, returns empty."""
    items = load_all()
    return next((item for item in items if item["food_item_id"] == food_id), None)

def filter_food_items(restaurant_id: int = None, course: str = None):
    """filter_food_items() retrieves food items with optional filtering by restaurant_id and course; returns list of matching items."""
    items = load_all()
    if restaurant_id:
        items = [item for item in items if item["restaurant_id"] == restaurant_id]
    if course:
        items = [item for item in items if item["course"].lower() == course.lower()]
    return items

def update_food_item(food_id: int, payload: FoodItemUpdate):
    """update_food_item() updates an existing food item with provided data; only fields with values will be updated and if item not found, returns none."""
    items = load_all()
    for item in items:
        if item["food_item_id"] == food_id:
            update_data = payload.model_dump(exclude_unset=True)
            item.update(update_data)
            save_all(items)
            return item
    return None

def delete_food_item(food_id: int) -> bool:
    """delete_food_item() deletes a food item by ID; returns true if successful, false if item not found."""
    items = load_all()
    initial_count = len(items)
    filtered_items = [item for item in items if item["food_item_id"] != food_id]

    if len(filtered_items) == initial_count:
        return False
    
    save_all(filtered_items)
    return True