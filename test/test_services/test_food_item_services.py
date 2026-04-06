import pytest
from decimal import Decimal
from app.services.food_item_service import create_food_item, delete_food_item
from app.schemas.food_item import FoodItemCreate
from app.schemas.inventory import InventoryCreate

def test_create_food_item_with_inventory(mocker): 
    """Tests that a food item is created and an ID is assigned with it, and inventory is initialized."""

    mocker.patch("app.services.food_item_service.load_all", return_value=[])
    mocker.patch("app.services.food_item_service.save_all")

    mock_inventory = mocker.patch("app.services.food_item_service.inventory_service.create_inventory_record")

    def fake_load_restaurants():
        return [{"restaurant_id": 1, "restaurant_name": "Dominos"}]

    import app.services.food_item_service as service
    service.load_restaurants = fake_load_restaurants

    payload = FoodItemCreate (
        food_name="Cheesecake",
        restaurant_id= 1,
        price=Decimal("7.0"),
        description="Fluffy original cheesecake",
        course="dessert",
    )

    new_item = create_food_item(payload)

    assert new_item["food_item_id"] == 1
    assert new_item["food_name"] == "Cheesecake"

    mock_inventory.assert_called_once_with(InventoryCreate(food_item_id = 1, quantity = 0))

def test_delete_food_item_with_inventory(mocker):
    """tests that deleting a food item will also delete the inventory"""
    mock_items = [{"food_item_id": 1, "food_name": "Cheesecake"}]
    mocker.patch("app.services.food_item_service.load_all", return_value=mock_items)
    mocker.patch("app.services.food_item_service.save_all")

    mock_inventory_cleanup = mocker.patch("app.services.food_item_service.inventory_service.delete_inventory_record")

    result = delete_food_item(1)

    assert result is True
    mock_inventory_cleanup.assert_called_once_with(1)