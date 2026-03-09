import pytest
import csv, os
from typing import List, Dict, Any
from app.repositories.order_items_repo import load_all, save_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "order_items.csv"
    
    mock_path.write_text("order_item_id,order_id,food_item_id,quantity,price_per_item\n"
                        "1,1,1,1,10.50\n"
                        "5cf89d5c-7ad2-4e03-856a-28cbb24e0591,a3a24e38-1f57-431a-ab30-58f2b6a2cf08,food1,1,4.0\n"
                        "7,3,1,1,12.50\n")

    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 3
    assert result[1]["order_item_id"] == "5cf89d5c-7ad2-4e03-856a-28cbb24e0591,a3a24e38-1f57-431a-ab30-58f2b6a2cf08"
    assert result[2]["order_id"] == "3"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "order_items.csv"
    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "order_items.csv"
    mock_path.write_text("order_item_id,order_id,food_item_id,quantity,price_per_item\n")
    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "order_items.csv"
    mock_path.write_text("order_item_id,order_id,food_item_id,quantity,price_per_item\n"
                        "1,1,1,1,10.50\n"
                        "5cf89d5c-7ad2-4e03-856a-28cbb24e0591,a3a24e38-1f57-431a-ab30-58f2b6a2cf08,food1,1,4.0\n"
                        "7,3,1,1,12.50\n")

    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)
    
    input_data = [{"order_item_id" : "1",
                "order_id" : "2",
                "food_item_id" : "3",
                "quantity" : "4",
                "price_per_item" : "5.0"}]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["order_item_id"] == "1"
    assert rows[0]["food_item_id"] == "3"
    assert rows[0]["price_per_item"] == "5.0"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "order_items.csv"
    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["order_item_id,order_id,food_item_id,quantity,price_per_item"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "order_items.csv"

    monkeypatch.setattr("app.repositories.order_items_repo.DATA_PATH", mock_path)
    input_data = [{"order_item_id" : "1",
                "order_id" : "2",
                "food_item_id" : "456",
                "quantity" : "4",
                "price_per_item" : "5.0"}]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["food_item_id"] == "456"