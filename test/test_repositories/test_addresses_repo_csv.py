import pytest
import csv

from app.repositories.addresses_repo_csv import load_all, save_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "addresses.csv"
    
    mock_path.write_text("address_id,user_id,street,city,postal_code,instructions,created_date\n"
                    "1,1,StreetNo,Kelowna,V1U 9U9,leave at door,2025-02-20T12:34:56\n"
                    "2,1,StreetNo,Kelowna,V1U 9U9,say hello to my cats,2025-02-20T12:34:56\n")

    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 2
    assert result[0]["address_id"] == "1"
    assert result[1]["city"] == "Kelowna"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "addresses.csv"
    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "addresses.csv"
    mock_path.write_text("address_id,user_id,street,city,postal_code,instructions,created_date\n")
    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "addresses.csv"   
    mock_path.write_text("address_id,user_id,street,city,postal_code,instructions,created_date\n"
                    "1,1,StreetNo,Kelowna,V1U 9U9,leave at door,2025-02-20T12:34:56\n"
                    "2,1,StreetNo,Kelowna,V1U 9U9,say hello to my cats,2025-02-20T12:34:56\n")
    
    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)
    
    input_data = [{
            "address_id": "1a2b3c",
            "user_id": "456",
            "street": "123 Brandybuck Lane",
            "city": "Tuckburough",
            "postal_code": "H0B 1T5",
            "instructions": "leave at door",
            "created_date": "2025-01-01"
        }]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["address_id"] == "1a2b3c"
    assert rows[0]["instructions"] == "leave at door"
    assert rows[0]["created_date"] == "2025-01-01"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "addresses.csv"
    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["address_id","user_id","street","city","postal_code","instructions","created_date"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "addresses.csv"

    monkeypatch.setattr("app.repositories.addresses_repo_csv.DATA_PATH", mock_path)
    input_data = [{
            "address_id": "1a2b3c",
            "user_id": "456",
            "street": "123 Brandybuck Lane",
            "city": "Tuckburough",
            "postal_code": "H0B 1T5",
            "instructions": "leave at door",
            "created_date": "2025-01-01"
        }]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["postal_code"] == "H0B 1T5"
    assert rows[0]["street"] == "123 Brandybuck Lane"