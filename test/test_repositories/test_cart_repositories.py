from unittest.mock import patch
import app.repositories.cart_repo_csv as repo
import pytest

def test_load_all_with_valid(mocker):
    """Creates valid fake load all mock data and ensures the values equal what they should"""
    mock_data = ("cart_id,customer_id\n"
            "76d5aa2e-d908-4fe2-b2ce-a67abf97e862,2")

    mocker.patch("app.repositories.cart_repo_csv.Path.open", mocker.mock_open(read_data=mock_data))
    result = repo.load_all()
    assert result[0]["cart_id"] == "76d5aa2e-d908-4fe2-b2ce-a67abf97e862"
   

def test_load_all_with_empty_file(mocker):
    """Creates empty fake load all mock data and ensures it returns empty data correctly"""

    mocker.patch("app.repositories.cart_repo_csv.Path.open", read_data="")
    result = repo.load_all()
    assert result == []


def test_load_all_with_empty_fields(mocker):
    """Creates fake load all mock data with empty fields and ensures it returns data correctly even when all fields are empty."""
    mock_data = ("cart_id,customer_id\n"
            ",")
    mocker.patch("app.repositories.cart_repo_csv.Path.open", mocker.mock_open(read_data=mock_data))
    result = repo.load_all()

    assert result[0]["cart_id"] == ""
    assert result[0]["customer_id"] == ""


def test_save_all_with_valid(tmp_path):
    """Creates valid fake save all data and ensures it saves this data properly"""
    mock_path = tmp_path/ "cart.csv"
    
    repo.DATA_PATH = mock_path
    
    mock_data = [
        {
            "cart_id": "8880136a-403b-4749-b612-jj0f0f8d2538",
            "customer_id": "1"
        }
    ]

    repo.save_all(mock_data)
    with open(mock_path, "r", encoding = "utf-8") as f: 
        saved = f.read()

    assert "8880136a-403b-4749-b612-jj0f0f8d2538" in saved


def test_save_all_invalid_format_data(tmp_path):
    """Creates wrong format of data"""
    mock_path = tmp_path/ "cart.csv"
    
    repo.DATA_PATH = mock_path
    
    invalid_data = {"cart_id": 1}
 
    with pytest.raises(ValueError, match = "Data needs to be a list"):
        repo.save_all(invalid_data)