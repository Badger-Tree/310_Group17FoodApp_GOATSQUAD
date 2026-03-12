from fastapi import HTTPException
import pytest

def test_update_cart_item_valid(mocker):
    expected_result = { 
        "food_item_id": 2,
        "quantity": 5,
        "price_per_item": "3.0",
        "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
        "cart_id": "3",
        "subtotal": "15.0"
    }

    mock_router = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_router.return_value = expected_result

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 3.0
        }
    
    result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", cart_update_data)

    assert result == expected_result


def test_update_cart_item_id_not_found(mocker):
    cart_item_id = "999"
    responseDetail = f"Cart Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 3.0}
   
    with pytest.raises(HTTPException) as httpExc:
        update_cart_item(cart_item_id, cart_update_data)
   

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


def test_update_cart_item_invalid(mocker):
    expected_result = { 
        "food_item_id": 2,
        "quantity": 5,
        "price_per_item": "3.0",
        "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
        "cart_id": "3",
        "subtotal": "15.0"
    }

    mock_router = mocker.patch("app.routers.cartItems.update_cart_item")
    mock_router.return_value = expected_result

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": "5",
        "price_per_item": "3.0"
        }
    
    result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3", cart_update_data)

    assert result == expected_result


def test_update_cart_item_id_zero():
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": 0,
        "price_per_item": 2.0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data)


def test_update_cart_item_id_zeros():
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"

    from app.routers.cartItems import update_cart_item
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data)
   