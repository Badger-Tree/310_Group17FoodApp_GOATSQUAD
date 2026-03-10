from app.routers.cartItems import get_cart_item_id
from fastapi import HTTPException
import pytest

def test_get_cart_item_id_valid(mocker):
    mock_router = mocker.patch("app.routers.cartItems.get_cartItem_by_id")
    mock_router.return_value = {"cart_item_id": "300"}
    result = get_cart_item_id("300")

    assert result["cart_item_id"] == "300"


def test_get_cart_item_id_not_found(mocker):
    cart_item_id = "999"
    mock_router = mocker.patch("app.routers.cartItems.get_cartItem_by_id")
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        get_cart_item_id("999")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail



        
