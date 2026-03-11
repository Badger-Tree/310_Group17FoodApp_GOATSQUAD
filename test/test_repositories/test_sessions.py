import pytest
import csv, os
from typing import List, Dict, Any
from app.repositories.sessions_repo import load_all, save_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "sessions.csv"
    
    mock_path.write_text("token,userid,role,created,expires\n"
                    "1,1,CUSTOMER,2026-02-20T12:34:56,2026-03-20T12:34:56\n"
                    "1a3ba654-2bd8-496c-847e-31e398e266fa,2,CUSTOMER,2026-02-20T12:34:56,2027-02-20T12:34:56\n")

    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 2
    assert result[0]["userid"] == "1"
    assert result[1]["userid"] == "2"
    assert result[1]["created"] == "2026-02-20T12:34:56"
def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "sessions.csv"
    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "sessions.csv"
    mock_path.write_text("id,email,first_name,last_name,password,role,created_date\n")
    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "sessions.csv"
    mock_path.write_text("token,userid,role,created,expires\n"
                    "1,1,CUSTOMER,2026-02-20T12:34:56,2026-03-20T12:34:56\n"
                    "1a3ba654-2bd8-496c-847e-31e398e266fa,2,CUSTOMER,2026-02-20T12:34:56,2027-02-20T12:34:56\n")

    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)
    
    input_data = [{"token" : "13",
                "userid" : "44",
                "role" : "CUSTOMER",
                "created" : "2026-02-20T12:34:56",
                "expires" : "2026-03-20T12:34:56"}]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["userid"] == "44"
    assert rows[0]["role"] == "CUSTOMER"
    assert rows[0]["created"] == "2026-03-20T12:34:56"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "sessions.csv"
    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["token","userid","role","created","expires"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "sessions.csv"

    monkeypatch.setattr("app.repositories.sessions_repo.DATA_PATH", mock_path)
    input_data = [{"token" : "13",
                "userid" : "44",
                "role" : "CUSTOMER",
                "created" : "2026-02-20T12:34:56",
                "expires" : "2026-03-20T12:34:56"}]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["userid"] == "44"
    