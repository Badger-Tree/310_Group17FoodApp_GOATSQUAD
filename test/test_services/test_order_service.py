from unittest import result
from unittest.mock import MagicMock

from app.schemas.Address import AddressResponse
import pytest
from fastapi import HTTPException
from datetime import datetime, timezone
from app.schemas.Delivery import DeliveryResponse
from app.schemas.Order import OrderResponse
from app.schemas.OrderItem import OrderItemResponse
from app.schemas.OrderStatus import OrderStatus
from app.schemas.cart_item_schema import CartItemResponse
from app.schemas.cart_schema import CartResponse
from app.services.cart_service import get_cart_by_customer
from app.services.order_service import accept_order_service, build_order, build_order_items, calculate_total, cancel_order_customer_service, get_order_by_order_id_service, get_order_status_by_id_service, get_orders_by_restaurant_service, get_orders_by_userid_service,cancel_order_restaurant_service, handle_payment, save_order, save_order_items, validate_restaurant_from_cart, process_order_service, set_order_status_service, validate_address, validate_cart
from app.services.order_service import get_order_history_service

mock_address_response = AddressResponse(address_id= "7",
            user_id= "cust456",
            street= "111 Shire Lane",
            city= "Hobbiton",
            postal_code= "H0B 1T5",
            instructions= "leave at driveway",
            created_date = "2025-01-20T11:34:56")
mock_delivery = DeliveryResponse(
    delivery_id="delivery123",
    order_id="order123",
    address_id="address123",
    courier_id=None,
    created_date=datetime.now()
)

def test_get_order_by_order_id_service_success(mocker):
    """tests that get_order_by_order_id_service() will successfully get an order given valid order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_order_by_order_id_service("order123")
    
    assert result.order_id == "order123"
    assert result.restaurant_id == 789
    assert result.created_date == datetime.fromisoformat("2026-02-20T12:34:56")
    assert result.items[0].food_item_id ==1
    assert result.items[1].food_item_id ==2

def test_get_order_by_order_id_service_order_not_found(mocker):
    """tests that get_order_by_order_id_service() will return empty object if order id not found"""

    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
    }]
        
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_order_by_order_id_service("order1")
    assert result is None
    
def mock_delivery_response():
    return 
    
def test_get_orders_by_restaurant_service_success(mocker):
    """tests that get_orders_by_restaurant_service() will successfully get an order given valid restaurant id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_orders_by_restaurant_service(789)
    assert len(result) == 1
    assert result[0].order_id=="order123"
    assert len(result[0].items) == 2
    assert result[0].items[0].food_item_id ==1
    assert result[0].items[1].food_item_id ==2
    
def test_get_orders_by_restaurant_service_not_found(mocker):
    """tests that get_orders_by_restaurant_service() will will return empty object if restaurant id not found"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    result = get_orders_by_restaurant_service("666")
    assert result == []
    
def test_get_orders_by_userid_service_success(mocker):
    """tests that get_orders_by_userid_service() will successfully get an order given valid user id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]
    mock_order_items = [{
                    "food_item_id": 1,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    },{
                    "food_item_id": 2,
                    "quantity" : 1,
                    "price_per_item" : "1.00",
                    "order_item_id" : "1",
                    "order_id" : "order123"
                    }]
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)

    result = get_orders_by_userid_service("cust456")
    assert len(result) == 1
    assert result[0].order_id=="order123"
    assert len(result[0].items) == 2
    
def test_get_orders_by_userid_service_not_found(mocker):
    """tests that get_orders_by_userid_service() will generate error if userid not found"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)

    result = get_orders_by_userid_service("616")
    assert result == []

def test_validate_cart_success(mocker):
    """tests that validate cart will return a cart given valid input"""
    
    mock_current_cart = [{
        "customer_id": "2",
        "cart_id": "GHDJDKSLAJ",
        "cart_items": [{
                "cart_item_id": "01KM8SQ4JB61NVWKSM2AVSFN3C",
                "food_item_id": 2,
                "quantity": 3,
                "price_per_item": 5.99,
                "subtotal": 17.97},{
                "cart_item_id": "61NVWKSM2AVSFDFKSLAJA",
                "food_item_id": 1,
                "quantity": 1,
                "price_per_item": 15.5,
                "subtotal": 15.5}],
        "total": 33.47}]
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_current_cart)
    result = validate_cart("2")
    assert result.customer_id == "2"
    assert result.cart_id == "GHDJDKSLAJ"
    assert result.cart_items[0].cart_item_id == "01KM8SQ4JB61NVWKSM2AVSFN3C"
    assert result.total == 33.47

def test_validate_cart_empty(mocker):
    """tests that validate cart will return an error given empty cart"""
    
    mock_data1 = [{ 
    "customer_id": "2", 
    "cart_id": "GHDJDKSLAJ",
    "cart_items": [],
    "total": 0
    }]
    mocker.patch("app.services.cart_service.load_all_carts", return_value = mock_data1)
    with pytest.raises(HTTPException) as testException: validate_cart("2")
    assert testException.value.status_code ==400

def validate_restaurant_from_cart_success(mocker):
    """tests that validate_restaurant_from_cart will return a restaurant id if given valid input"""
    
    class MockItem:
        def __init__(self, food_item_id):
            self.food_item_id = food_item_id

    class MockCart:
        def __init__(self):
            self.cart_items = [MockItem(1), MockItem(2)]
    mock_cart = MockCart()
    mocker.patch(
        "app.services.order_service.get_food_by_id",
        side_effect=[
            {"restaurant_id": 10},
            {"restaurant_id": 10},
            {"restaurant_id": 10},
        ]
    )
    result = validate_restaurant_from_cart(mock_cart)
    assert result == 10

def test_validate_restaurant_from_cart_multiple_items(mocker):
    """tests that validate_restaurant_from_cart will return a restaurant id if given valid input"""
    class MockItem:
        def __init__(self, food_item_id):
            self.food_item_id = food_item_id

    class MockCart:
        def __init__(self):
            self.cart_items = [MockItem(1), MockItem(2)]
    mock_cart = MockCart()
    mocker.patch("app.services.order_service.get_food_by_id",side_effect=[
            {"restaurant_id": 10},
            {"restaurant_id": 11},
            {"restaurant_id": 10},
        ]
    )
    with pytest.raises(HTTPException) as testException: validate_restaurant_from_cart(mock_cart)
    assert testException.value.status_code ==400

def test_validate_address_success(mocker):
    """tests that validate_address will return an address given valid input"""
    mock_addresses = AddressResponse(
        address_id= "1",
        user_id= "456",
        street= "111 Shire Lane",
        city= "Hobbiton",
        postal_code= "H0B 1T5",
        instructions= "leave at driveway",
        created_date= "2025-01-20T11:34:56")
    mocker.patch("app.services.order_service.get_address_by_id_service", return_value = mock_addresses)
    result = validate_address("1")
    assert result.address_id == "1"
    assert result.user_id == "456"
    assert result.city == "Hobbiton"
    
def test_validate_address_not_found(mocker):
    """tests that validate_address will return an error if it can't find the provided address"""

    mocker.patch("app.services.order_service.get_address_by_id_service", side_effect=HTTPException(status_code=404))
    with pytest.raises(HTTPException) as testException: validate_address("999")
    assert testException.value.status_code ==404

def test_calculate_total_success(mocker):
    mock_current_cart = CartResponse(
    customer_id="cust_12345",
    cart_id="cart_abc123",
    cart_items=[
        CartItemResponse(
            cart_item_id="item_1",
            food_item_id=101,
            quantity=2,
            price_per_item=9.99,
            subtotal=19.98,
        ),
        CartItemResponse(
            cart_item_id="item_2",
            food_item_id=202,
            quantity=1,
            price_per_item=5.49,
            subtotal=5.49,
        ),
    ],
    total=25.47,
)
    result = calculate_total(mock_current_cart)
    assert result == 25.47

def test_build_order_success(mocker):
    """tests that build order will compose a dictionary with valid input"""
    mock_current_cart = CartResponse(
    customer_id="cust_123",
        cart_id="cart_abc123",
        cart_items=[
            CartItemResponse(
                cart_item_id="item_1",
                food_item_id=101,
                quantity=2,
                price_per_item=9.99,
                subtotal=19.98,
            ),
        ],
        total=25.47,
    )
    mock_address_id = "1"
    mock_total = 25.47
    mock_restaurant_id = 100;
    
    result = build_order(mock_current_cart, mock_total, mock_address_id, mock_restaurant_id)
    assert result["customer_id"] == "cust_123"
    assert result["restaurant_id"] == 100
    assert result["delivery_id"] is None
    assert result["status"] == "PENDING"
  
def test_build_order_items(mocker):
    """tests that build order items will compose a dictionary with valid input"""
    mock_current_cart = CartResponse(
        customer_id="cust_12345",
        cart_id="cart_abc123",
        cart_items=[
            CartItemResponse(
                cart_item_id="item_1",
                food_item_id=101,
                quantity=2,
                price_per_item=9.99,
                subtotal=19.98,
            ),
            CartItemResponse(
                cart_item_id="item_2",
                food_item_id=202,
                quantity=1,
                price_per_item=5.49,
                subtotal=5.49,
            ),
        ],
        total=25.47,
    )
    mock_order_id = "1"
    result = build_order_items(mock_current_cart, mock_order_id)
    assert len(result) == 2
    assert result[0]["order_id"] == "1"
    assert result[0]["food_item_id"] == 101

def test_handle_payment_success(mocker):
    """tests that handle_payment will send a payment and notification if given valid input"""
    test_order_dict={"order_id": "1",
                "customer_id": "2",
                "restaurant_id": 100,
                "cart_id": "cart",
                "delivery_id" : None,
                "status" : "PENDING",
                "total_amount" : 100.00,
                "created_date" : datetime.now(timezone.utc),
                "delivery_address_id" : "1"}
    mock_payment = mocker.patch("app.services.order_service.process_payment_service",return_value = True)
    mock_notify= mocker.patch("app.services.order_service.notify_payment_status")
    result = handle_payment(test_order_dict)
    assert result is True
    mock_payment.assert_called_once_with(100.00)
    mock_notify.assert_called_once_with("2", "1", True)
    
    
def test_handle_payment_payment_failed(mocker):
    """tests that handle_payment will return an error if payment fails"""
    test_order_dict={"order_id": "1",
                "customer_id": "2",
                "restaurant_id": 100,
                "cart_id": "cart",
                "delivery_id" : None,
                "status" : "PENDING",
                "total_amount" : 100.00,
                "created_date" : datetime.now(timezone.utc),
                "delivery_address_id" : "1"}
    mock_payment = mocker.patch("app.services.order_service.process_payment_service",return_value = False)
    mock_notify= mocker.patch("app.services.order_service.notify_payment_status")

    with pytest.raises(HTTPException) as testException: handle_payment(test_order_dict)
    assert testException.value.status_code ==400
    mock_payment.assert_called_once_with(100.00)
    mock_notify.assert_called_once_with("2", "1", False)

def test_save_order_success(mocker):
    """tests that save_order will save a new order to repo"""
    existing_data = [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "345",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": datetime(2026, 2, 20, 12, 34, 56),
        "delivery_address_id": "addr202"
    }]
    new_order = {
        "order_id": "order124",
        "customer_id": "cust789",
        "restaurant_id": 101,
        "cart_id": "cart102",
        "delivery_id": "346",
        "status": "PENDING",
        "total_amount": 15.99,
        "created_date": datetime(2026, 2, 21, 13, 0, 0),
        "delivery_address_id": "addr203"
    }

    mock_load = mocker.patch("app.services.order_service.load_orders", return_value=existing_data)
    mock_save = mocker.patch("app.services.order_service.save_all_orders")

    save_order(new_order)
    saved_orders = mock_save.call_args[0][0]
    assert isinstance(saved_orders, list)
    assert len(saved_orders) > 1

def test_save_order_items_success(mocker):
    """tests that save_order_items will save new order items to repo"""
    existing_data = [{"order_item_id": "item001",
                        "order_id": "order123",
                        "food_item_id": 10,
                        "quantity": 2,
                        "price_per_item": 5.0
    }]
    new_items = [{
            "order_id": "order124",
            "food_item_id": 11,
            "quantity": 1,
            "price_per_item": 7.5
    }]

    mock_load = mocker.patch("app.services.order_service.load_order_items", return_value=existing_data)
    mock_save = mocker.patch("app.services.order_service.save_all_order_items")

    save_order_items(new_items)
    saved_orders = mock_save.call_args[0][0]
    assert isinstance(saved_orders, list)
    assert len(saved_orders) > 1

def test_process_order_success(mocker):
    """tests that process_order will route information to all services it calls given customer and address"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=25.47,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = [{"order_id": "order124", "food_item_id": 11, "quantity": 1, "price_per_item": 7.5}]
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="abc123",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )

    mocker.patch("app.services.order_service.validate_item_inventory")
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.get_cart_by_customer", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", return_value=mock_address)
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.handle_payment")
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.clear_cart")

    result = process_order_service(customer_id, address_id)
    assert result.order_id == "1"
    assert result.customer_id == customer_id
    assert result.items[0].food_item_id == 11
    
def test_process_order_payment_failed(mocker):
    """tests that process_order will route information to all services it calls given customer and address"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="cart_abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=25.47,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = [{"order_id": "order124", "food_item_id": 11, "quantity": 1, "price_per_item": 7.5}]
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="cart",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )
    mocker.patch("app.services.order_service.validate_item_inventory")
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", return_value=mock_address)
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.handle_payment", side_effect=HTTPException(status_code=400))
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")

    with pytest.raises(HTTPException) as testException: process_order_service(customer_id, address_id)
    assert testException.value.status_code ==400
    
def test_process_order_service_insufficient_inventory(mocker):
    """checks that method raises 422 exception if a cart items do not have sufficient inventory"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="cart_abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=25.47,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = []
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="cart",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )
    mocker.patch("app.services.order_service.validate_item_inventory",side_effect=HTTPException(status_code=422))
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", return_value=mock_address)
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")

    with pytest.raises(HTTPException) as testException: process_order_service(customer_id, address_id)
    assert testException.value.status_code ==422
        
def test_process_order_service_empty_cart(mocker):
    """checks that method raises 400 exception if a cart has no items in it"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="cart_abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=25.47,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = []
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="cart",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )
    mocker.patch("app.services.order_service.validate_item_inventory")
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", return_value=mock_address)
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.handle_payment", side_effect=HTTPException(status_code=400))
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")

    with pytest.raises(HTTPException) as testException: process_order_service(customer_id, address_id)
    assert testException.value.status_code ==400
    

def test_process_order_service_address_not_found(mocker):
    """checks that method raises 404 exception there is no address matching input id"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="cart_abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=25.47,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = []
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="cart",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )

    mocker.patch("app.services.order_service.validate_item_inventory")
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", side_effect=HTTPException(status_code=404))
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mock_build_order = mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mock_build_order_items = mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mock_payment = mocker.patch("app.services.order_service.handle_payment")
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")

    with pytest.raises(HTTPException) as testException: process_order_service("cart123","nocart")
    assert testException.value.status_code ==404
    mock_payment.assert_not_called()
    mock_build_order.assert_not_called()
    mock_build_order_items.assert_not_called()

def test_process_order_service_multiple_items(mocker):
    """tests that process_order will route information to all services it calls given customer and address with multiple order items"""
    customer_id = "2"
    address_id = "addr_456"
    mock_cart = CartResponse(
        customer_id=customer_id,
        cart_id="cart_abc123",
        cart_items=[CartItemResponse(cart_item_id="item_1", food_item_id=101, quantity=2, price_per_item=9.99, subtotal=19.98),
                    CartItemResponse(cart_item_id="item_2", food_item_id=102, quantity=2, price_per_item=9.99, subtotal=19.98)],
        total=39.96,
    )
    mock_address = MagicMock()
    mock_address.address_id = address_id
    mock_order_items = [{"order_id": "order124", "food_item_id": 11, "quantity": 1, "price_per_item": 7.5}]
    mock_order_response = OrderResponse(
        order_id="1",
        customer_id=customer_id,
        restaurant_id=100,
        cart_id="cart",
        delivery_id=None,
        status="PENDING",
        total_amount=100.0,
        created_date=datetime.now(timezone.utc),
        delivery_address_id=address_id,
        items=[OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5),
               OrderItemResponse(order_id="order124", food_item_id=11, order_item_id="111", quantity=1, price_per_item=7.5)],
    )
    mocker.patch("app.services.order_service.validate_item_inventory")
    mocker.patch("app.services.order_service.validate_cart", return_value=mock_cart)
    mocker.patch("app.services.order_service.validate_restaurant_from_cart", return_value="rest_101")
    mocker.patch("app.services.order_service.validate_address", return_value=mock_address)
    mocker.patch("app.services.order_service.calculate_total", return_value=100.0)
    mocker.patch("app.services.order_service.build_order", return_value={"order_id": "1"})
    mocker.patch("app.services.order_service.build_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.handle_payment")
    mocker.patch("app.services.order_service.save_order")
    mocker.patch("app.services.order_service.save_order_items")
    mocker.patch("app.services.order_service.get_order_by_order_id_service", return_value=mock_order_response)
    mocker.patch("app.services.order_service.notify_order_placed")
    mocker.patch("app.services.order_service.clear_cart")

    result = process_order_service(customer_id, address_id)
    assert result.order_id == "1"
    assert result.customer_id == customer_id
    assert result.items[0].food_item_id == 11
    assert len(result.items) == 2
    
def test_cancel_order_restaurant_service_success(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "345",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": datetime(2026, 2, 20, 12, 34, 56),
                    "delivery_address_id": "addr202"
        }]
    def mock_save_orders(input):
        return input
    mocker.patch("app.services.order_service.add_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders", mock_save_orders)
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    result = cancel_order_restaurant_service("order123")
    assert result.order_id == ("order123")
    
def test_cancel_order_restaurant_service_refund_failed(mocker):
    """tests that cancel_order_restaurant_service() will successfully cancel an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mocker.patch("app.services.order_service.add_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.notify_refund_issued")
    mocker.patch("app.services.order_service.notify_order_status_update")
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels")
    mocker.patch("app.services.order_service.process_refund_service", return_value=False)
    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order123")
    assert testException.value.status_code ==400
    
def test_cancel_order_restaurant_service_order_not_found(mocker):
    """tests that cancel_order_restaurant_service() will generate an error if order is not found by order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mocker.patch("app.services.order_service.add_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    with pytest.raises(HTTPException) as testException: cancel_order_restaurant_service("order1")
    assert testException.value.status_code ==404

def test_get_order_status_by_id_service_success(mocker):
    """tests that get_order_status_by_id_service will return an Order status given a valid order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "CANCELED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    
    result = get_order_status_by_id_service("order123")
    assert result == OrderStatus.CANCELED
    
def test_get_order_status_by_id_service_order_not_found(mocker):
    """tests that get_order_status_by_id_service will return a 404 exception if it cannot find the given order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
    }]

    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    with pytest.raises(HTTPException) as testException: get_order_status_by_id_service("noorder")
    assert testException.value.status_code ==404
    
def test_set_order_status_service_success(mocker):
    """tests that set_order_status will change the status of an order given a valid order id and status"""

    mock_orders= [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "delivery",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": "2026-02-20T12:34:56",
        "delivery_address_id": "addr202"
        }]

    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders", mock_save_orders)
    
    result = set_order_status_service("order123",OrderStatus.ACCEPTED)
    assert result.status == OrderStatus.ACCEPTED

def test_set_order_status_service_order_not_found(mocker):
    """tests that set_order_status will raise a 404 error if the order is not found"""

    mock_orders= [{
        "order_id": "order123",
        "customer_id": "cust456",
        "restaurant_id": 789,
        "cart_id": "cart101",
        "delivery_id": "delivery",
        "status": "PENDING",
        "total_amount": 26.66,
        "created_date": "2026-02-20T12:34:56",
        "delivery_address_id": "addr202"
        }]

    def mock_save_orders(input):
        return input
    
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    with pytest.raises(HTTPException) as testException: set_order_status_service("noorder",OrderStatus.ACCEPTED)
    assert testException.value.status_code ==404
    
def test_cancel_order_customer_success(mocker):
    """tests that cancel_order_customer_service() will cancel an order given valid input"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": datetime(2026, 2, 20, 12, 34, 56),
                    "delivery_address_id": "addr202"
        }]
    def mock_save_orders(input):
        return input
    mocker.patch("app.services.order_service.add_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value=mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels", return_value=None)

    mocker.patch("app.services.order_service.load_order_items", return_value=[{
        "order_id": "order123",
        "order_item_id" : "1",
        "food_item_id": 1,
        "quantity": 2,
        "price_per_item": 13.33
    }])
    result = cancel_order_customer_service("order123")
    assert result.order_id == ("order123")  

def test_cancel_order_customer_service_completed(mocker):
    """tests that cancel_order_customer_service() will generate an error if order has already been completed"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "COMPLETED",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]

    mocker.patch("app.services.order_service.add_stock", return_value=None)
    mocker.patch("app.services.order_service.process_refund_service", return_value=True)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.notify_refund_issued", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update_customer_cancels", return_value=None)
    with pytest.raises(HTTPException) as testException: cancel_order_customer_service("order123")
    assert testException.value.status_code ==400

def test_accept_order_service_success(mocker):
    """tests that accept_order_service() will successfully accept an order given valid order id from restaurant side"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mock_order_items = [{
        "food_item_id": 1,
        "quantity" : 1,
        "price_per_item" : "1.00",
        "order_item_id" : "1",
        "order_id" : "order123"
    }]
    mocker.patch("app.services.order_service.create_delivery_service", return_value=mock_delivery)
    mocker.patch("app.services.order_service.subtract_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.load_order_items", return_value = mock_order_items)
    mocker.patch("app.services.order_service.save_all_order_items")
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.clear_cart")
    result = accept_order_service("order123")
    assert result.status == OrderStatus.ACCEPTED 
    
def test_accept_order_service_order_not_found(mocker):
    """tests that accept_order_service() will generate an error if order is not found by order id"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": None,
                    "status": "PENDING",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mocker.patch("app.services.order_service.create_delivery_service", return_value=mock_delivery)
    mocker.patch("app.services.order_service.subtract_stock", return_value=None)
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.clear_cart")
    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404

def test_accept_order_service_accepted(mocker):
    """tests that accept_order_service() will generate an error if order has already been accepted"""
    mock_orders= [{
                    "order_id": "order123",
                    "customer_id": "cust456",
                    "restaurant_id": 789,
                    "cart_id": "cart101",
                    "delivery_id": "delivery",
                    "status": "IN_PREPARATION",
                    "total_amount": 26.66,
                    "created_date": "2026-02-20T12:34:56",
                    "delivery_address_id": "addr202"
        }]
    mocker.patch("app.services.order_service.create_delivery_service", return_value=mock_delivery)
    mocker.patch("app.services.order_service.subtract_stock", return_value=None)
    mocker.patch("app.services.order_service.load_orders", return_value = mock_orders)
    mocker.patch("app.services.order_service.save_all_orders")
    mocker.patch("app.services.order_service.notify_order_status_update", return_value=None)
    mocker.patch("app.services.order_service.clear_cart")
    with pytest.raises(HTTPException) as testException: accept_order_service("order1")
    assert testException.value.status_code ==404

#Testing for order history
def test_get_order_history_service_default_success(mocker):
    """Tests that get_order_history_service() successfully returns a list of OrderHistoryResponse objects with valid input and default parameters"""
    
    mock_orders = [
        {
            "order_id": "1",
            "customer_id": "1",
            "restaurant_id": 100,
            "cart_id": "cart1",
            "delivery_id": "delivery1",
            "status": "COMPLETED",
            "total_amount": 20.0,
            "created_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "delivery_address_id": "addr1"
        },
        {
            "order_id": "2",
            "customer_id": "2",
            "restaurant_id": 101,
            "cart_id": "cart2",
            "delivery_id": "delivery2",
            "status": "CANCELED",
            "total_amount": 15.0,
            "created_date": datetime(2024, 1, 2, tzinfo=timezone.utc),
            "delivery_address_id": "addr2"
        },
        {
            "order_id": "3",
            "customer_id": "1",
            "restaurant_id": 102,
            "cart_id": "cart3",
            "delivery_id": "delivery3",
            "status": "PENDING",
            "total_amount": 30.0,
            "created_date": datetime(2024, 1, 3, tzinfo=timezone.utc),
            "delivery_address_id": "addr3"
        }
    ]

    mock_order_items = [
        {
            "order_item_id": "item1",
            "order_id": "1",
            "food_item_id": 10,
            "quantity": 2,
            "price_per_item": 10.0
        },
        {
            "order_item_id": "item2",
            "order_id": "2",
            "food_item_id": 11,
            "quantity": 1,
            "price_per_item": 15.0
        },
        {
            "order_item_id": "item3",
            "order_id": "3",
            "food_item_id": 12,
            "quantity": 3,
            "price_per_item": 10.0
        }
    ]

    mock_restaurants = [
        {
            "restaurant_id": 100,
            "restaurant_name": "Mario's Pizzeria",
            "cuisine": "Italian",
        },
        {
            "restaurant_id": 101,
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese"
        },
        {
            "restaurant_id": 102,
            "restaurant_name": "Tesh test restaurant",
            "cuisine": "Test"
        }
    ]

    mocker.patch("app.services.order_service.load_orders", return_value=mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.load_restaurants", return_value=mock_restaurants)

    result = get_order_history_service("1")

    assert len(result) == 2

    assert result[0].order_id == "3"
    assert result[0].restaurant_name == "Tesh test restaurant"
    assert result[0].items[0].food_item_id == 12

    assert result[1].order_id == "1"
    assert result[1].restaurant_name == "Mario's Pizzeria"
    assert result[1].items[0].food_item_id == 10

def test_get_order_history_service_filter_accepted_true(mocker):
    """Tests that get_order_history_service() returns only accepted orders."""

    mock_orders = [
        {
            "order_id": "1",
            "customer_id": "1",
            "restaurant_id": 100,
            "cart_id": "cart1",
            "delivery_id": "delivery1",
            "status": "ACCEPTED",
            "total_amount": 20.0,
            "created_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "delivery_address_id": "addr1"
        },
        {
            "order_id": "2",
            "customer_id": "1",
            "restaurant_id": 101,
            "cart_id": "cart2",
            "delivery_id": "delivery2",
            "status": "PENDING",
            "total_amount": 15.0,
            "created_date": datetime(2024, 1, 2, tzinfo=timezone.utc),
            "delivery_address_id": "addr2"
        }
    ]

    mock_order_items = [
        {
            "order_item_id": "item1",
            "order_id": "1",
            "food_item_id": 10,
            "quantity": 2,
            "price_per_item": 10.0
        },
        {
            "order_item_id": "item2",
            "order_id": "2",
            "food_item_id": 11,
            "quantity": 1,
            "price_per_item": 15.0
        }
    ]

    mock_restaurants = [
        {
            "restaurant_id": 100,
            "restaurant_name": "Mario's Pizzeria",
            "cuisine": "Italian",
        },
        {
            "restaurant_id": 101,
            "restaurant_name": "Sakura Sushi",
            "cuisine": "Japanese"
        }
    ]

    mocker.patch("app.services.order_service.load_orders", return_value=mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.load_restaurants", return_value=mock_restaurants)

    result = get_order_history_service("1", accepted=True)

    assert len(result) == 1
    assert result[0].order_id == "1"
    assert result[0].status == OrderStatus.ACCEPTED
    assert result[0].restaurant_name == "Mario's Pizzeria"
    assert result[0].items[0].food_item_id == 10

def test_get_order_history_service_invalid_sort_order(mocker):
    """Tests that get_order_history_service() raises an HTTPException for an invalid sort order."""

    mock_orders = [
        {
            "order_id": "1",
            "customer_id": "1",
            "restaurant_id": 100,
            "cart_id": "cart1",
            "delivery_id": "delivery1",
            "status": "ACCEPTED",
            "total_amount": 20.0,
            "created_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "delivery_address_id": "addr1"
        }
    ]

    mock_order_items = [
        {
            "order_item_id": "item1",
            "order_id": "1",
            "food_item_id": 10,
            "quantity": 2,
            "price_per_item": 10.0
        }
    ]

    mock_restaurants = [
        {
            "restaurant_id": 100,
            "restaurant_name": "Mario's Pizzeria",
            "cuisine": "Italian",
        }
    ]

    mocker.patch("app.services.order_service.load_orders", return_value=mock_orders)
    mocker.patch("app.services.order_service.load_order_items", return_value=mock_order_items)
    mocker.patch("app.services.order_service.load_restaurants", return_value=mock_restaurants)

    with pytest.raises(HTTPException) as exc_info:
        get_order_history_service("1", sort_order="wrong")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid sort order. Must be 'asc' or 'desc'."
