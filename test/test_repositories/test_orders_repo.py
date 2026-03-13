import pytest
import csv, os
from typing import List, Dict, Any
from app.repositories.orders_repo import load_all, save_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "orders.csv"
    
    mock_path.write_text("order_id,customer_id,restaurant_id,cart_id,delivery_id,status,total_amount,created_date,delivery_address_id\n"
                    "order123,cust456,rest123,cart101,,APPROVED,26.66,2026-02-20T12:34:56,addr202\n"
                    "order456,cust456,rest789,cart101,,PENDING,26.66,2026-02-20T12:34:56,addr202n")

    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 2
    assert result[0]["order_id"] == "order123"
    assert result[1]["order_id"] == "order456"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "orders.csv"
    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "orders.csv"
    mock_path.write_text("id,email,first_name,last_name,password,role,created_date\n")
    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "orders.csv"
    mock_path.write_text("order_id,customer_id,restaurant_id,cart_id,delivery_id,status,total_amount,created_date,delivery_address_id\n"
                    "order123,cust456,rest123,cart101,,APPROVED,26.66,2026-02-20T12:34:56,addr202\n"
                    "order456,cust456,rest789,cart101,,PENDING,26.66,2026-02-20T12:34:56,addr202n")

    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)
    
    input_data = [{"order_id" : "1",
                "customer_id" : "2",
                "restaurant_id" : "3",
                "cart_id" : "4",
                "delivery_id" : "5",
                "status" : "PENDING",
                "created_date" : "2025-01-01",
                "delivery_address_id" : "6"}]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["customer_id"] == "2"
    assert rows[0]["status"] == "PENDING"
    assert rows[0]["created_date"] == "2025-01-01"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "orders.csv"
    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["order_id","customer_id","restaurant_id","cart_id","delivery_id","status","total_amount","created_date","delivery_address_id"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "orders.csv"

    monkeypatch.setattr("app.repositories.orders_repo.DATA_PATH", mock_path)
    input_data = [{"order_id" : "1",
                "customer_id" : "2",
                "restaurant_id" : "3",
                "cart_id" : "4",
                "delivery_id" : "5",
                "status" : "PENDING",
                "created_date" : "2025-01-01",
                "delivery_address_id" : "6"}]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["delivery_id"] == "5"