import pytest
from pydantic import ValidationError
from app.schemas.inventory import InventoryCreate, InventoryUpdate

def test_inventory_create_valid():
    """Will test that valid data creates a successful InventoryCreate instance."""
    data = {
        "food_item_id": 400,
        "quantity": 10
    }
    schema = InventoryCreate(**data)
    assert schema.food_item_id == 400
    assert schema.quantity == 10

def test_inventory_create_negative_quantity():
    """Will test that a negative quantity raises a ValidationError."""
    with pytest.raises(ValidationError):
        InventoryCreate(food_item_id=400, quantity=-5)

def test_inventory_create_invalid_types():
    """Tests that non-int values raises a ValidationError."""
    with pytest.raises(ValidationError):
        InventoryCreate(food_item_id="not_an_int", quantity=10)

def test_inventory_create_default_quantity():
    """Tests that quantity defaults to 0 if not given."""
    data = {"food_item_id": 400}
    schema = InventoryCreate(**data)
    assert schema.food_item_id == 400
    assert schema.quantity == 0

def test_inventory_update_partial():
    """This tests that InventoryUpdate allows updating only the quantity"""
    update_data = {"quantity": 30}
    schema = InventoryUpdate(**update_data)
    assert schema.quantity == 30