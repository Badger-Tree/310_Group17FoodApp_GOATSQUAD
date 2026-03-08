import pytest
import csv, os
from typing import List, Dict, Any
from app.repositories.users_repo_csv import load_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "users.csv"
    
    mock_path.write_text("id,email,first_name,last_name,password,role,created_date\n"
                    "1,tame@example.com,spongebob,string,string,CUSTOMER,2026-02-20T12:34:56\n"
                    "1a3ba654-2bd8-496c-847e-31e398e266fa,pippin@example.com,pippin,werner,string,CUSTOMER,2026-03-06T04:14:49.252383+00:00\n")

    monkeypatch.setattr("app.repositories.users_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "1a3ba654-2bd8-496c-847e-31e398e266fa"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "users.csv"
    monkeypatch.setattr("app.repositories.users_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    mock_path = tmp_path / "users.csv"
    mock_path.write_text("id,email,first_name,last_name,password,role,created_date\n")
    monkeypatch.setattr("app.repositories.users_repo_csv.DATA_PATH", mock_path)
    
    result = load_all()
    
    assert result == []