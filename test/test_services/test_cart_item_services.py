from app.services.cartItems_service import add_cart_item

def test_add_cart_item_valid(mocker):

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

    result = add_cart_item(cartItem_data)

    assert result.food_item_id == 3
    assert result.quantity == 3
    assert result.price_per_item == 10.0
    assert result.cart_id == sample_cart_id
    assert result.cart_item_id == sample_cart_item_id
    assert result.address_id == "3"
    assert result.subtotal == 30.0



def test_add_cart_item_does_not_exist(mocker):

    cartItem_data = {
        "food_item_id": 3,
        "quantity": 3,
        "customer_id": "1"
    }


    mock_load_all = mocker.patch("app.services.cartItems_service.load_all")
    mock_load_all.return_value = []

    mock_uuid = mocker.patch("app.services.cartItems_service.uuid.uuid4")
    mock_uuid.side_effect = ["newCartIDGenerated", "newCartItemIDGenerated"]

    result = add_cart_item(cartItem_data)

    assert result.food_item_id == 3
    assert result.quantity == 3
    assert result.price_per_item == 10.0
    assert result.cart_id == "newCartIDGenerated"
    assert result.cart_item_id == "newCartItemIDGenerated"
    assert result.address_id == "1"
    assert result.subtotal == 30.0



