import csv
import pytest
from app.repositories import inventory_repository

def test_save_and_load_all(tmp_path):
    """verifies that it writes a list of dictionaries and reads them back exactly as they are"""
    original_path = inventory_repository.DATA_PATH
    test_csv = tmp_path / "inventory_test.csv"
    inventory_repository.DATA_PATH = test_csv

    test_data = [
        {"inventory_id": "1", "food_item_id": "101", "quantity": "10"},
        {"inventory_id": "2", "food_item_id": "102", "quantity": "20"}
    ]

    inventory_repository.save_all(test_data)
    loaded_data = inventory_repository.load_all()

    assert len(loaded_data) == 2
    assert loaded_data[0]["food_item_id"] == "101"
    assert loaded_data[1]["quantity"] == "20"

    inventory_repository.DATA_PATH = original_path