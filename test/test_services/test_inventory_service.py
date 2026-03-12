import pytest
from unittest.mock import patch
from app.services import inventory_service
from app.schemas.inventory import Inventory

@patch("app.services.inventory_service.inventory_repository.get_inventory_by_food_id")
def test_check_availability_true(mock_get_inventory):
    """checks availability returns True when sufficient stock exists"""
    mock_get_inventory.return_value = Inventory(inventory_id=1, food_item_id=101, quantity=10)

    result = inventory_service.check_availability(food_item_id=101, quantity=5)

    assert result is True
    mock_get_inventory.assert_called_once_with(101)

@patch("app.services.inventory_service.inventory_repository.get_inventory_by_food_id")
def test_check_availability_false(mock_get_inventory):
    """checks availability returns False when stock is insufficient"""
    mock_get_inventory.return_value = Inventory(inventory_id=1, food_item_id=101, quantity=2)
    result = inventory_service.check_availability(food_item_id=101, quantity=5)

    assert result is False

def test_update_stock_negative_raises_error():
    """Test that updating stock with a negative quantity raises a ValueError"""
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        inventory_service.update_stock(food_item_id=101, new_quantity=-5)