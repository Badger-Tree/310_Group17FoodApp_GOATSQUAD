from unittest.mock import patch
import app.repositories.cart_items_repo_csv as repo
import pytest

def test_load_all_with_valid(mocker):
    """Creates valid load all mock data and ensures the values equal what they should"""
    mock_data = ("cart_item_id,food_item_id,price_per_item,quantity,subtotal\n"
            "FHDSJFKSJF,1,6.0,1,6.0")

    with mocker.patch("app.repositories.cart_items_repo_csv.Path.exists", return_value=True):
        mocker.patch("app.repositories.cart_items_repo_csv.Path.open", mocker.mock_open(read_data=mock_data))
    result = repo.load_all()
    assert result[0]["cart_item_id"] == "FHDSJFKSJF"
   

def test_load_all_with_empty_file(mocker):
    """Creates empty load all mock data and ensures it returns empty data correctly"""
    with mocker.patch("app.repositories.cart_items_repo_csv.Path.exists", return_value=True):
        mocker.patch("app.repositories.cart_items_repo_csv.Path.open", mocker.mock_open(read_data=""))
    result = repo.load_all()
    assert result == []


def test_load_all_with_empty_fields(mocker):
    """Creates load all mock data with empty fields and ensures it returns data correctly even when all fields are empty."""
    mock_data = ("cart_item_id,food_item_id,price_per_item,quantity,subtotal\n"
            ",,,,")
    with mocker.patch("app.repositories.cart_items_repo_csv.Path.exists", return_value=True):
        mocker.patch("app.repositories.cart_items_repo_csv.Path.open", mocker.mock_open(read_data=mock_data))
    result = repo.load_all()

    assert result[0]["cart_item_id"] == ""
    assert result[0]["food_item_id"] == ""
    assert result[0]["quantity"] == ""
    assert result[0]["price_per_item"] == ""
    assert result[0]["subtotal"] == ""


def test_save_all_with_valid(tmp_path):
    """Creates valid fake save all data and ensures it saves this data properly"""
    mock_path = tmp_path/ "cartItems.csv"
    
    repo.DATA_PATH = mock_path
    
    mock_data = [
        {
            "cart_item_id": "FHSJFKSJFGKA",
            "food_item_id": 10,
            "quantity": 1,
            "price_per_item": 6.0,
            "subtotal": 6.0
        }
    ]

    repo.save_all(mock_data)
    with open(mock_path, "r", encoding = "utf-8") as f: 
        saved = f.read()

    assert "FHSJFKSJFGKA" in saved


def test_save_all_invalid_format_data(tmp_path):
    """Creates wrong format of data and ensures in raises an error"""
    mock_path = tmp_path/ "cartItems.csv"
    
    repo.DATA_PATH = mock_path
    
    invalid_data = {"cart_item_id": "FHSJFKSJFGKA"}
 
    with pytest.raises(ValueError, match = "Data should be a list"):
        repo.save_all(invalid_data)