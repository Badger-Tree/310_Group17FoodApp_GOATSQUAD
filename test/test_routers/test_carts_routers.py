from app.routers.carts import get_items_by_cart
from fastapi import HTTPException
import pytest

def get_items_by_cart_route(mocker):
    mock_router = mocker.patch("app.routers.cart.get_items_by_cart")
    mock_router.return_value = {"cart_id": "300"}
    result = get_items_by_cart("300")

    assert result["cart_id"] == "300"


def get_items_by_cart_route(mocker):
    cart_id = "999"
    mock_router = mocker.patch("app.routers.cart.get_items_by_cart")
    responseDetail = f"Item '{cart_id}' not found"
    statusCode = 404
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
   
    with pytest.raises(HTTPException) as httpExc:
        get_items_by_cart("999")

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail