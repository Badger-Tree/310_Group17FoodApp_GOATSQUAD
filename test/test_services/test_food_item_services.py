from decimal import Decimal
from app.services.food_item_service import create_food_item, delete_food_item
from app.schemas.food_item import FoodItemCreate

def test_create_food_item(): 
    """Tests that a food item is created and an ID is automatically assigned."""
    payload = FoodItemCreate (
        food_name="Cheesecake",
        restaurant_id=2,
        price=Decimal("7.0"),
        description="Fluffy original cheesecake",
        course="dessert",
    )

    new_item = create_food_item(payload)

    assert new_item["food_name"] == "Cheesecake"
    assert new_item["price"] == Decimal("7.0")
    assert new_item["description"] == "Fluffy original cheesecake"
    assert new_item["course"] == "dessert"


    assert "food_item_id" in new_item
    assert isinstance(new_item["food_item_id"], int)

    delete_food_item(new_item["food_item_id"])