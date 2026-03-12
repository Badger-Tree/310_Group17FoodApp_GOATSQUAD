from unittest.mock import patch
import app.repositories.cartItems_repo as repo
import pytest
import json

def test_load_all_with_valid(mocker):
    mock_data = [
        {
            "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
            "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
            "food_item_id": 10,
            "quantity": 1,
            "price_per_item": 6.0,
            "subtotal": 6.0
        }
    ]

    mocker.patch("app.repositories.cartItems_repo.load_all", return_value = mock_data)
    result = repo.load_all()
    assert result[0]["cart_item_id"] == "7950136a-403b-4749-b612-ff0f0f8d2338"
    assert result[0]["cart_id"] == "0fe8ea74-fdff-4088-9e27-3ce23b0b3432"
    assert result[0]["food_item_id"] == 10
    assert result[0]["quantity"] == 1
    assert result[0]["price_per_item"] == 6.0 
    assert result[0]["subtotal"] == 6.0


def test_load_all_with_empty_file(mocker):
    mock_data = []

    mocker.patch("app.repositories.cartItems_repo.load_all", return_value = mock_data)
    result = repo.load_all()
    assert result == []

def test_load_all_with_empty_file(mocker):
    mock_data = [
          {
            "cart_item_id": None,
            "cart_id": None,
            "food_item_id": None,
            "quantity": None,
            "price_per_item": None,
            "subtotal": None
        }
    ]

    mocker.patch("app.repositories.cartItems_repo.load_all", return_value = mock_data)
    result = repo.load_all()
    assert result == mock_data





def test_save_all_with_valid(tmp_path):
    mock_path = tmp_path/ "cartItems.json"
    
    repo.DATA_PATH = mock_path
    
    mock_data = [
        {
            "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
            "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
            "food_item_id": 10,
            "quantity": 1,
            "price_per_item": 6.0,
            "subtotal": 6.0
        }
    ]

    repo.save_all(mock_data)
    with open(mock_path, "r", encoding = "utf-8") as f: 
        saved = json.load(f)

    assert saved == mock_data


def test_save_all_invalid_data_raises(tmp_path):
    mock_path = tmp_path/ "cartItems.json"
    
    repo.DATA_PATH = mock_path
    
    invalid_data = [{"cart_item_id": {1, 10, "3"}}]
    
    import pytest
    with pytest.raises(TypeError):
        repo.save_all(invalid_data)