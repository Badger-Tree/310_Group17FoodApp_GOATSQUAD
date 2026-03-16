import pytest
import csv, os
from typing import List, Dict, Any
from app.repositories.deliveries_repo_csv import load_all, save_all, DATA_PATH

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "deliveries.csv"
    
    mock_path.write_text("order_id,courier_id,created_date,address_id,delivery_status,delivery_id\n"
                        "1,1,2024-01-01,1,delivered,1\n"
                        "2,2,2024-01-02,2,in_transit,2\n"
                        "3,3,2024-01-03,3,pending,3\n")

    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 3
    assert result[1]["order_id"] == "2"
    assert result[2]["order_id"] == "3"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "deliveries.csv"
    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "deliveries.csv"
    mock_path.write_text("order_id,courier_id,created_date,address_id,delivery_status,delivery_id\n")
    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "deliveries.csv"
    mock_path.write_text("order_id,courier_id,created_date,address_id,delivery_status,delivery_id\n"
                        "1,1,2024-01-01,1,delivered,1\n"
                        "2,2,2024-01-02,2,in_transit,2\n"
                        "3,3,2024-01-03,3,pending,3\n")

    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)
    
    input_data = [{"order_id" : "1",
                "courier_id" : "2",
                "created_date" : "2024-01-01",
                "address_id" : "1",
                "delivery_status" : "delivered",
                "delivery_id" : "1"}]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["order_id"] == "1"
    assert rows[0]["courier_id"] == "2"
    assert rows[0]["created_date"] == "2024-01-01"
    assert rows[0]["address_id"] == "1"
    assert rows[0]["delivery_status"] == "delivered"
    assert rows[0]["delivery_id"] == "1"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "deliveries.csv"
    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["order_id", "courier_id", "created_date", "address_id", "delivery_status", "delivery_id"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "deliveries.csv"

    monkeypatch.setattr("app.repositories.deliveries_repo_csv.DATA_PATH", mock_path)
    input_data = [{"order_id" : "1",
                "courier_id" : "2",
                "created_date" : "2024-01-01",
                "address_id" : "1",
                "delivery_status" : "delivered",
                "delivery_id" : "1"}]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["courier_id"] == "2"
    assert rows[0]["created_date"] == "2024-01-01"
    assert rows[0]["address_id"] == "1"
    assert rows[0]["delivery_status"] == "delivered"
    assert rows[0]["delivery_id"] == "1"