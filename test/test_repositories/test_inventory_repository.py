import csv
import pytest
from app.repositories import inventory_repository
from app.schemas.inventory import InventoryCreate, InventoryUpdate

def create_mock_csv(file_path, data):
    """Helper function to create a temporary CSV file with the given data"""
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["inventory_id", "food_item_id", "quantity"])
        writer.writeheader()
        writer.writerows(data)
    return file_path


def test_create_inventory_record(tmp_path):
    """Test creating a new inventory record and verify it is saved correctly"""
    original_path = inventory_repository.DATA_PATH
    inventory_repository.DATA_PATH = tmp_path / "inventory_test.csv"

    try:
        payload = InventoryCreate(food_item_id=600, quantity=20)
        result = inventory_repository.create_inventory_record(payload)

        assert result.food_item_id == 600
        assert result.quantity == 20
        assert result.inventory_id == 1  

    finally:
        inventory_repository.DATA_PATH = original_path


def test_get_inventory_by_food_id_success(tmp_path):
    """Test retrieving an existing inventory record by food_item_id"""
    original_path = inventory_repository.DATA_PATH
    test_csv = tmp_path / "inventory_test.csv"
    inventory_repository.DATA_PATH = test_csv

    try:
        initial_data = [
            {"inventory_id": 1, "food_item_id": 300, "quantity": 50}
        ]
        create_mock_csv(test_csv, initial_data)

        result = inventory_repository.get_inventory_by_food_id(300)

        assert result is not None
        assert result.food_item_id == 300
        assert result.quantity == 50

    finally:
        inventory_repository.DATA_PATH = original_path


def test_get_inventory_by_food_id_not_found(tmp_path):
    """Test retrieving a non-existent inventory record by food_item_id returns None"""
    original_path = inventory_repository.DATA_PATH
    inventory_repository.DATA_PATH = tmp_path / "empty.csv"

    try:
        result = inventory_repository.get_inventory_by_food_id(999)
        assert result is None
    finally:
        inventory_repository.DATA_PATH = original_path


def test_update_inventory_record_success(tmp_path):
    """Test updating an existing inventory record's quantity and verify the change is saved, while other records remain unchanged"""
    original_path = inventory_repository.DATA_PATH
    test_csv = tmp_path / "inventory_test.csv"
    inventory_repository.DATA_PATH = test_csv

    try:
        initial_data = [
            {"inventory_id": 1, "food_item_id": 300, "quantity": 50},
            {"inventory_id": 2, "food_item_id": 400, "quantity": 30}
        ]
        create_mock_csv(test_csv, initial_data)

        update_payload = InventoryUpdate(quantity=75)
        result = inventory_repository.update_inventory(300, update_payload)

        assert result.quantity == 75
        other_item = inventory_repository.get_inventory_by_food_id(400)
        assert other_item.quantity == 30
    finally:        
        inventory_repository.DATA_PATH = original_path


def test_delete_inventory_record_success(tmp_path):
    """Test deleting an existing inventory record by food_item_id and verify it is removed from the CSV file"""
    original_path = inventory_repository.DATA_PATH
    test_csv = tmp_path / "inventory_test.csv"
    inventory_repository.DATA_PATH = test_csv

    try:
        initial_data = [
            {"inventory_id": 1, "food_item_id": 300, "quantity": 50}]
        create_mock_csv(test_csv, initial_data)

        success = inventory_repository.delete_inventory_record(300)
        assert success is True
        assert inventory_repository.get_inventory_by_food_id(300) is None
    finally:
        inventory_repository.DATA_PATH = original_path