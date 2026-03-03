from ..schemas.food_item import FoodItemCreate, FoodItemUpdate
from ..repositories.food_item_repo import load_all, save_all

def list_food_items():
    return load_all()

def create_food_item(payload: FoodItemCreate):
    items = load_all()

    #generate new ids by finding curr highest id + 1; if empty list, start @ 1 
    new_id = max([item["food_item_id"] for item in items], default=0) + 1

    #create new obj using data from payload + new id
    new_food = payload.model_dump()
    new_food["food_item_id"] = new_id

    items.append(new_food)
    save_all(items)
    return new_food

def get_food_by_id(food_id: int):
    items = load_all()
    return next((item for item in items if item["food_item_id"] == food_id), None)

#filter list by restaurant_id and course
def filter_food_items(restaurant_id: int = None, course: str = None):
    items = load_all()
    if restaurant_id:
        items = [item for item in items if item["restaurant_id"] == restaurant_id]
    if course:
        #.lower() to make searching case-insensitive
        items = [item for item in items if item["course"].lower() == course.lower()]
    return items

def update_food_item(food_id: int, payload: FoodItemUpdate):
    items = load_all()
    for item in items:
        if item["food_item_id"] == food_id:
            #update fields that were sent
            update_data = payload.model_dump(exclude_unset=True)
            item.update(update_data)
            save_all(items)
            return item
    return None

def delete_food_item(food_id: int) -> bool:
    items = load_all()
    initial_count = len(items)
    #filter out item to be deleted
    filtered_items = [item for item in items if item["food_item_id"] != food_id]

    #if counts are same, nothing was deleted
    if len(filtered_items) == initial_count:
        return False
    
    save_all(filtered_items)
    return True