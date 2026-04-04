import pytest
import csv, os
from app.repositories.reviews_repo import load_all, save_all

def test_load_all_success(monkeypatch, tmp_path):
    """tests that load_all() will return a  list with data from csv data that csv exists, has data"""
    mock_path = tmp_path / "reviews.csv"
    
    mock_path.write_text("review_id,restaurant_id,customer_id,review,rating\n"
                         "1,1,456,good food,4\n"
                         "2,1,789,okay,2\n")

    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)
    result = load_all()
    assert len(result) == 2
    assert result[0]["review_id"] == "1"
    assert result[0]["restaurant_id"] == "1"
    assert result[0]["customer_id"] == "456"
    assert result[0]["review"] == "good food"
    assert result[0]["rating"] == "4"

def test_load_all_fileDNE(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file that does not exist"""
    mock_path = tmp_path / "reviews.csv"
    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []

def test_load_all_empty(monkeypatch, tmp_path):
    """this tests that load_all() will return an empty list if calling a file with no records"""
    mock_path = tmp_path / "reviews.csv"
    mock_path.write_text("review_id,restaurant_id,customer_id,review,rating\n")
    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)
    result = load_all()
    assert result == []
    
def test_save_all_success(monkeypatch, tmp_path):
    """this tests that save_all() will overwrite input to a csv if csv exists and has headers"""
    mock_path = tmp_path / "reviews.csv"
    mock_path.write_text("review_id,restaurant_id,customer_id,review,rating\n"
                        "1,1,456,good food,4\n"
                        "2,1,789,okay,2\n")

    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)
    
    input_data = [{"review_id" : "1",
                "customer_id" : "2",
                "restaurant_id" : "3",
                "review" : "4",
                "rating" : "5"}]
    
    save_all(input_data)
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["review_id"] == "1"
    assert rows[0]["customer_id"] == "2"
    assert rows[0]["restaurant_id"] == "3"
    assert rows[0]["review"] == "4"
    assert rows[0]["rating"] == "5"
    
def test_save_all_empty_list(monkeypatch, tmp_path):
    """this tests that save_all() will save input to a csv if csv exists and has no header row"""
    mock_path = tmp_path / "reviews.csv"
    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)

    save_all([])
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 0
    expected_fields = ["review_id","restaurant_id","customer_id","review","rating"]
    assert reader.fieldnames == expected_fields
    
def test_save_all_fileDNE(monkeypatch, tmp_path):
    """tests that save_all still works if the csv does not yet exist"""
    mock_path = tmp_path / "reviews.csv"

    monkeypatch.setattr("app.repositories.reviews_repo.DATA_PATH", mock_path)
    input_data = [{"review_id" : "1",
                "customer_id" : "2",
                "restaurant_id" : "3",
                "review" : "4",
                "rating" : "5"}]
    
    save_all(input_data)
    assert mock_path.exists()
    
    with mock_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["review_id"] == "1"
    assert rows[0]["customer_id"] == "2"
    assert rows[0]["restaurant_id"] == "3"
    assert rows[0]["review"] == "4"
    assert rows[0]["rating"] == "5"