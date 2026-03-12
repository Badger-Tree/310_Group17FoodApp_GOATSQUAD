from app.schemas.cart import CartBase, CartResponse, ListCartResponse
from pydantic import ValidationError
import pytest


def test_CartBase_valid(): 

    cart_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0
    }

    result = CartBase(**cart_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0


def test_CartBase_missing_input(): 

    cart_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0
    }
    with pytest.raises(ValidationError):
       CartBase(**cart_data)




def test_CartItemResponse_valid(): 

    cart_data = { 
        "food_item_id": 1,
        "quantity": 3,
        "price_per_item": 2.0,
        "cart_item_id": "31",
        "cart_id": "12", 
        "subtotal": 6.0
    }

    result = CartResponse(**cart_data)
    assert result.food_item_id == 1
    assert result.quantity == 3
    assert result.price_per_item == 2.0
    assert result.cart_item_id == "31"
    assert result.cart_id == "12"
    assert result.subtotal == 6.0


def test_CartResponse_missing_input(): 

    cart_data = { 
        "food_item_id": 1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": "400",
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)


def test_CartResponse_zero_value(): 

    cart_data = { 
        "food_item_id": 1,
        "quantity": 0,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)

def test_CartResponse_negative_value(): 

    cart_data = { 
        "food_item_id": 1,
        "quantity": -1,
        "price_per_item": 2.0,
        "cart_item_id": "200",
        "cart_id": 400,
        "subtotal": 2.0
    }
    with pytest.raises(ValidationError):
       CartResponse(**cart_data)




def test_ListCartResponse_valid(): 

    cartItem_data = {
  
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

    result = ListCartResponse(**cartItem_data)
    assert result.cartList[0].food_item_id == 10
    assert result.cartList[0].quantity == 1
    assert result.cartList[0].price_per_item == 6
    assert result.cartList[0].cart_item_id == "7950136a-403b-4749-b612-ff0f0f8d2338"
    assert result.cartList[0].cart_id == "0fe8ea74-fdff-4088-9e27-3ce23b0b3432"
    assert result.cartList[0].subtotal == 6

    assert result.cartList[1].food_item_id == 16
    assert result.cartList[1].quantity == 2
    assert result.cartList[1].price_per_item == 6
    assert result.cartList[1].cart_item_id == "4"
    assert result.cartList[1].cart_id == "0fe8ea74-fdff-4088-9e27-3ce23b0b3432"
    assert result.cartList[1].subtotal == 12

    assert result.total == 18.0


def test_ListCartResponse_missing_input(): 

    cartItem_data = {
 
  "cartList": [
    {
      "food_item_id": 10,
      "cart_item_id": "7950136a-403b-4749-b612-ff0f0f8d2338",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 6
    },
    {
      "quantity": 2,
      "price_per_item": 6,
      "cart_item_id": "4",
      "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
      "subtotal": 12
    }
  ],
  "total": 18.0
}
    with pytest.raises(ValidationError):
       CartBase(**cartItem_data)

       