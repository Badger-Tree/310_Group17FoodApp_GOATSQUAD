from datetime import datetime
from pydantic import ValidationError
import pytest
from app.schemas.Order import  OrderCreate, OrderBase, OrderResponse
from app.schemas.OrderItem import OrderItemCreate, OrderItemResponse # type: ignore


# def test_OrderItemBase_valid():
# def test_OrderItemBase_invalid_data():
# def test_OrderItemBase_missing_data():

# def test_OrderItemCreate_valid():
# def test_OrderItemCreate_invalid_data():
# def test_OrderItemCreate_missing_data():

# def test_OrderItemResponse_valid():
# def test_OrderItemResponse_invalid_data():
# def test_OrderItemResponse_missing_data():
