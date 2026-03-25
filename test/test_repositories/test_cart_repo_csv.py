from unittest.mock import patch
from app.schemas.cart_item_schema import CartItemResponse
import app.repositories.cart_repo_csv as repo
import pytest

def test_load_all_with_valid(mocker, tmp_path):
    """Creates valid load all mock data and ensures the values equal what they should"""
    mock_path = tmp_path / "cart.csv"

    mock_data = (
    'customer_id,cart_id,cart_items,total\n'
    '2,BDJSLAJDSK,"[{'
    '""customer_id"": ""2"", '
    '""cart_item_id"": ""HGJDKASHA"", '
    '""food_item_id"": 1, '
    '""quantity"": 1, '
    '""price_per_item"": 5.99, '
    '""total"": 5.99'
    '}]","5.99"\n'
)

    mock_path.write_text(mock_data)
    mocker.patch("app.repositories.cart_repo_csv.DATA_PATH", mock_path)
    
    result = repo.load_all()
    result[0]["customer_id"] == "2"
   

def test_load_all_with_empty_file(mocker, tmp_path):
    """Creates empty load all mock data and ensures it returns empty data correctly"""
    mock_path = tmp_path / "cart.csv"

    mock_data = ("")
    
    mock_path.write_text(mock_data)
    mocker.patch("app.repositories.cart_repo_csv.DATA_PATH", mock_path)
    
    result = repo.load_all()
    assert result == []


def test_load_all_with_empty_fields(mocker, tmp_path):
    """Creates load all mock data with empty fields and ensures it returns data correctly even when all fields are empty."""
    mock_path = tmp_path / "cart.csv"
    mock_data = ("cart_id,customer_id,cart_items,total\n"
            ",,,")
    
    mock_path.write_text(mock_data)
    mocker.patch("app.repositories.cart_repo_csv.DATA_PATH", mock_path)

    result = repo.load_all()

    assert result[0]["cart_id"] == ""
    assert result[0]["customer_id"] == ""
    assert result[0]["cart_items"] == []
    assert result[0]["total"] == 0.0


def test_save_all_with_valid(tmp_path):
    """Creates valid save all data and ensures it saves this data properly"""
    mock_path = tmp_path/ "cart.csv"
    
    repo.DATA_PATH = mock_path
    
    mock_data = [
        {
            "cart_id": "8880136a-403b-4749-b612-jj0f0f8d2538",
            "customer_id": "1",
            "cart_items": [
            CartItemResponse(
                cart_item_id = "01KM962C98K38KV1DARXPB8S21", 
                food_item_id = 2, 
                quantity = 3, 
                price_per_item = 5.99, 
                subtotal = 17.97)
                ],
            "total": "1"
        }
    ]

    repo.save_all(mock_data)
    with open(mock_path, "r", encoding = "utf-8") as f: 
        saved = f.read()

    assert "8880136a-403b-4749-b612-jj0f0f8d2538" in saved


def test_save_all_invalid_format_data(tmp_path):
    """Creates wrong format of data to ensure it raises an error"""
    mock_path = tmp_path/ "cart.csv"
    repo.DATA_PATH = mock_path
    
    invalid_data = {"cart_id": "FHSJFKSJFGKA"}
 
    with pytest.raises(ValueError, match = "Data should be a list"):
        repo.save_all(invalid_data)

