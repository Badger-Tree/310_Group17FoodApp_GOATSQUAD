import pytest
from fastapi import HTTPException
from app.routers.cartItems import get_cartItem_by_id, add_cart_item, update_cart_item, delete_cart_item
from unittest.mock import patch

mock_cart_data = [ 
    {
    "cart_item_id": "92075de6-2b6d-43b8-acef-4b69c3d962f7",
    "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
    "address_id": "3",
    "food_item_id": 34,
    "quantity": 1,
    "price_per_item": 4.0,
    "subtotal": 4.0
    },

    {
    "cart_item_id": "5",
    "cart_id": "0fe8ea74-fdff-4088-9e27-3ce23b0b3432",
    "address_id": "3",
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

def test_get_cartItem_by_id_valid(cart_item_id, expected):
    """Checks that the function returns the correct dictionary with valid data"""
    with patch("app.services.cartItems_service.load_all", return_value=mock_cart_data):
        result = get_cartItem_by_id(cart_item_id)
        assert result.model_dump() == expected


@pytest.mark.parametrize("cart_item_id", ["", " "])
def test_get_cartItem_by_id_empty(cart_item_id):
    """Checks that the function raises exception with empty or invalid input strings"""
    responseDetail = "cart_item_id cannot be empty"
    statusCode = 400
    with pytest.raises(HTTPException) as httpExc:
        get_cartItem_by_id(cart_item_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail
   
   
@pytest.mark.parametrize("cart_item_id", ["cart_item_id_not_found"])
def test_get_cartItem_by_wrong_id(cart_item_id):
    """Checks that the function raises exception if the cart_item_id cannot be found"""
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404
    with pytest.raises(HTTPException) as httpExc:
        get_cartItem_by_id(cart_item_id)

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail



def test_add_cart_item_valid(mocker):
    """Tests that the function returns proper data when adding a valid cart item"""

    cartItem_data = {
        "food_item_id": 3,
        "quantity": 3,
        "customer_id": "2"
    }

    sample_cart_id = "0fe8ea74-fdff-4088-9e27-3ce23b0b3432"
    sample_cart_item_id = "92075de6-2b6d-43b8-acef-4b69c3d962f7"

    mock_load_all = mocker.patch("app.services.cartItems_service.load_all")
    mock_load_all.return_value = []

    mock_uuid = mocker.patch("app.services.cartItems_service.uuid.uuid4")
    mock_uuid.side_effect = [sample_cart_id, sample_cart_item_id]

    mocker.patch(
        "app.services.cartItems_service.get_food_by_id",
        return_value={
            "food_item_id": 3,
            "price": 10.0
        }
    )

    mock_user = mocker.MagicMock()
    mock_user.id = "3"

    mocker.patch(
        "app.services.cartItems_service.get_user_from_session",
        return_value=mock_user
    )

    result = add_cart_item(cartItem_data)

    assert result.food_item_id == 3
    assert result.quantity == 3
    assert result.price_per_item == 10.0
    assert result.cart_id == sample_cart_id
    assert result.cart_item_id == sample_cart_item_id
    assert result.address_id == "4"
    assert result.subtotal == 30.0



def test_add_cart_item_does_not_exist(mocker):
    """Tests that the function returns proper data when an item is added to a cart that does not exists"""
    cartItem_data = {
        "food_item_id": 3,
        "quantity": 3,
        "customer_id": "1"
    }

    mock_load_all = mocker.patch("app.services.cartItems_service.load_all")
    mock_load_all.return_value = []

    mock_uuid = mocker.patch("app.services.cartItems_service.uuid.uuid4")
    mock_uuid.side_effect = ["newCartIDGenerated", "newCartItemIDGenerated"]

    mocker.patch(
        "app.services.cartItems_service.get_food_by_id",
        return_value={
            "food_item_id": 3,
            "price": 10.0
        }
    )

    mock_user = mocker.MagicMock()
    mock_user.id = "3"

    mocker.patch(
        "app.services.cartItems_service.get_user_from_session",
        return_value=mock_user
    )

    result = add_cart_item(cartItem_data)

    assert result.food_item_id == 3
    assert result.quantity == 3
    assert result.price_per_item == 10.0
    assert result.cart_id == "newCartIDGenerated"
    assert result.cart_item_id == "newCartItemIDGenerated"
    assert result.address_id == "4"
    assert result.subtotal == 30.0


def test_update_cart_item_valid():
    """Tests that the function returns proper data when updating with valid input"""
    
    payload = {
        "quantity": 1, 
        "price_per_item": 2.0
        }

    mock_data = [
        {
            "address_id": "5",
            "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
            "cart_id": "3",
            "food_item_id": 2,
            "quantity": 1,
            "price_per_item": 2.0,
            "subtotal": 2.0
        }
    ]

    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = update_cart_item("cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",payload["quantity"])  
    

    assert result.address_id == "5"
    assert result.cart_item_id == "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    assert result.cart_id == "3"
    assert result.food_item_id == 2
    assert result.quantity == 1
    assert result.price_per_item == 2.0
    assert result.subtotal == 2.0


def test_update_cart_item_id_not_found(mocker):
    """Tests function raises an error when the cart to update is not found"""
    cart_item_id = "999"
    responseDetail = f"Cart Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.services.cartItems_service.update_cartItem")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
    
    cart_update_data = { 
        "quantity": 5,
        "price_per_item": 3}
   
    with pytest.raises(HTTPException) as httpExc:
        update_cart_item(cart_item_id, cart_update_data["quantity"])
   
    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail


def test_update_cart_item_invalid():
    """Tests cart is properly updated even with inproper input i.e string instead of int"""
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    
    cart_update_data = { 
        "quantity": "5",
        "price_per_item": 2.0
        }
    
    mock_data = [
        {
            "address_id": "5",
            "cart_item_id": "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3",
            "cart_id": "3",
            "food_item_id": 2,
            "quantity": 5,
            "price_per_item": 2.0,
            "subtotal": 10.0
        }
    ]
   
    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = update_cart_item(cart_item_id,cart_update_data["quantity"])  
    

    assert result.address_id == "5"
    assert result.cart_item_id == "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    assert result.cart_id == "3"
    assert result.food_item_id == 2
    assert result.quantity == 5
    assert result.price_per_item == 2.0
    assert result.subtotal == 10.0


def test_update_cart_item_id_zero():
    """Tests that if the new quantity to be updated is zero it raises an error"""
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    
    cart_update_data = { 
        "quantity": 0,
        "price_per_item": 2.0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data["quantity"])


def test_update_cart_item_id_negative():
    """Tests that if the new quantity to be updated is less than zero it raises an error """
    cart_item_id = "cb3d05e3-24f6-4ba1-a5bb-6ba2db243fc3"
    
    cart_update_data = { 
        "quantity": -1,
        "price_per_item": 0
        }
   
    with pytest.raises(ValueError):
        update_cart_item(cart_item_id, cart_update_data["quantity"])



def test_remove_cartItem_valid(): 
    """Tests that the cart_item_id in question (if it exists) is removed"""
    cart_item_id = "7c67321e-3dda-4a69-bde4-baba0b7c7288"

    mock_data = [{
        "cart_item_id": cart_item_id,
        "cart_id": "e9fffefe-7287-46e4-a433-05f11c73e4a4",
        "customer_id": "2",
        "address_id": "3",
        "food_item_id": 1,
        "quantity": 1,
        "price_per_item": 15.5,
        "subtotal": 15.5
  }]
    
    with patch("app.services.cartItems_service.load_all", return_value=mock_data):
        result = delete_cart_item(cart_item_id)

    assert result == None


def test_remove_cartItem_invalid(mocker): 
    """Tests that if the cart does not exist when trying to remove it, it raises an exception"""

    cart_item_id = "7c67321e-3dda-4a69-bde4-baba0b7c7288"
    responseDetail = f"Item '{cart_item_id}' not found"
    statusCode = 404

    mock_router = mocker.patch("app.services.cartItems_service.update_cartItem")
    mock_router.side_effect = HTTPException(detail=responseDetail, status_code=statusCode)
    
    with pytest.raises(HTTPException) as httpExc:
        delete_cart_item(cart_item_id)
   

    assert httpExc.value.status_code == statusCode
    assert httpExc.value.detail == responseDetail
    
