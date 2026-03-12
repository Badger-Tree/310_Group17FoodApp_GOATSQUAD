from app.services.cart_service import get_items_by_cart
import pytest
from fastapi import HTTPException
from unittest.mock import patch

mock_cart_data = [ 
{
  "cartList": [
    {
      "food_item_id": 10,
      "quantity": 1,
      "price_per_item": 6,
      "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 6
    },
    {
      "food_item_id": 16,
      "quantity": 2,
      "price_per_item": 6,
      "cart_item_id": "4",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 12
    }
  ],
  "total": 18.0
}
]


expected_data = {
  "cartList": [
    {
      "food_item_id": 10,
      "quantity": 1,
      "price_per_item": 6,
      "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 6
    },
    {
      "food_item_id": 16,
      "quantity": 2,
      "price_per_item": 6,
      "cart_item_id": "4",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 12
    }
  ],
  "total": 18.0
}


with patch("app.services.cart_service.load_all", return_value = mock_cart_data):
    result = get_items_by_cart("0fe8ea74-fdff-4088-9e27-3ce23b0b3432")
    assert result == expected_data


mock_cart_data = [ 
{
  "cartList": [
    {
      "food_item_id": 10,
      "quantity": 1,
      "price_per_item": 6,
      "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
      "cart_id": 5,
      "subtotal": 6
    },
    {
      "food_item_id": 16,
      "quantity": 2,
      "price_per_item": 6,
      "cart_item_id": "4",
      "cart_id": 5,
      "subtotal": 12
    }
  ],
  "total": 18.0
}
]


expected_data = {
  "cartList": [
    {
      "food_item_id": 10,
      "quantity": 1,
      "price_per_item": 6,
      "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
      "cart_id": "5",
      "subtotal": 6
    },
    {
      "food_item_id": 16,
      "quantity": 2,
      "price_per_item": 6,
      "cart_item_id": "4",
      "cart_id": "5",
      "subtotal": 12
    }
  ],
  "total": 18.0
}

with patch("app.services.cart_service.load_all", return_value = mock_cart_data):
    result = get_items_by_cart(5)
    assert result == expected_data


@pytest.mark.parametrize("cart_id", ["", " "])
def test_get_items_by_cart_empty(cart_id):
    responseDetail = "cart_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_cart(cart_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


@pytest.mark.parametrize("cart_id", ["cart_id_not_found"])
def test_get_items_by_cart_id(cart_id):
    responseDetail = f"Cart '{cart_id}' not found"
    statusCode = 404
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_cart(cart_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail