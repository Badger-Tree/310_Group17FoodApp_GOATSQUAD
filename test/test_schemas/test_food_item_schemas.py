import pytest 
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate

def test_food_item_create_valid():
    """Tests that valid data creates a FoodItemCreate instance successfully."""
    data = {
        "food_name": "Apple",
        "restaurant_id": 555,
        "price": Decimal("0.99"),
        "description": "A fresh apple",
        "course": "Dessert",
    }

    schema = FoodItemCreate(**data)

    assert schema.food_name == "Apple"
    assert schema.restaurant_id == 555
    assert schema.price == Decimal("0.99")
    assert schema.description == "A fresh apple"
    assert schema.course == "Dessert"

def test_food_item_create_invalid_price():
    """Tests that an invalid price raises a ValidationError."""
    with pytest.raises(ValidationError):
        FoodItemCreate(
            food_name="Banana",
            restaurant_id=555,
            price="invalid_price", 
            description="A ripe banana",
            course="Dessert",
        )

def test_food_item_create_price_too_many_decimals():
    """Tests that a price with too many decimal places raises a ValidationError."""
    with pytest.raises(ValidationError):
        FoodItemCreate(
            food_name="Cherry",
            restaurant_id=555,
            price=Decimal("0.999"), 
            description="A sweet cherry",
            course="Main",
        )

def test_food_item_create_missing_required_field():
    """This tests that missing required fields will raise an error."""
    with pytest.raises(ValidationError):
        FoodItemCreate(
            restaurant_id=555,
            price=Decimal("0.99"),
            description="A sweet cherry",
            course="Main"
        )

def test_food_item_update_valid():
    """This tests that FoodItemUpdate allows partial updates of data and validates."""
    update_data = {"price": Decimal("1.49")}
    schema = FoodItemUpdate(**update_data)

    assert schema.price == Decimal("1.49")
    assert schema.food_name is None
    assert schema.description is None
    assert schema.course is None