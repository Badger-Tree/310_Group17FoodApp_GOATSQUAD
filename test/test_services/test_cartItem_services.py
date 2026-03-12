from app.services.cartItems_service import get_cartItem_by_id
import pytest
from fastapi import HTTPException
from unittest.mock import patch

mock_cart_data = [ 
{
    "cart_item_id": "92075de6-2b6d-43b8-acef-4b69c3d962f7",
    "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
    "food_item_id": 34,
    "quantity": 1,
    "price_per_item": 4.0,
    "subtotal": 4.0
},
    {
    "cart_item_id": "5",
    "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
    "food_item_id": 34,
    "quantity": 1,
    "price_per_item": 4.0,
    "subtotal": 4.0
    }
]

@pytest.mark.parametrize("cart_item_id, expected", [
    ("92075de6-2b6d-43b8-acef-4b69c3d962f7", mock_cart_data[0]),
    (5, mock_cart_data[1])

])

def test_get_cartItem_by_id(cart_item_id, expected):
    with patch("app.services.cartItems_service.load_all", return_value=mock_cart_data):
        result = get_cartItem_by_id(cart_item_id)
        assert result == expected


@pytest.mark.parametrize("cart_item_id", ["", " "])
def test_get_cartItem_by_id_empty(cart_item_id):
    responseDetail = "cart_item_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        get_cartItem_by_id(cart_item_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


@pytest.mark.parametrize("cart_item_id", ["cart_item_id_not_found"])
def test_get_cartItem_by_wrong_id(cart_item_id):
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404
    with pytest.raises(HTTPException) as httpExc:
        get_cartItem_by_id(cart_item_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail
