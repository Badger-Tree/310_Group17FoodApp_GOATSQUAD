from datetime import datetime
import pytest
from fastapi import HTTPException
from app.schemas.Address import Address, AddressCreate, AddressUpdate
from app.services.address_service import get_address_by_id_service, get_address_by_customer_id_service, create_address_service, update_address_service, delete_address_service

# def test_get_address_by_id_service_success(monkeypatch)
"""tests if get_address_by_id_service() gets address given valid input"""
# def test_get_address_by_id_service_id_not_found(monkeypatch)
"""tests if get_address_by_id_service() raises exception if addressid not found"""
# def test_get_address_by_id_service_invalid_input(monkeypatch)
"""tests if get_address_by_id_service() raises exception if given invalid input"""

# def test_get_address_by_customer_id_service_success(monkeypatch)
"""tests if get_address_by_customer_id_service() gets address given valid customer id input"""

# def test_get_address_by_customer_id_service_customer_not_found(monkeypatch)
"""tests if get_address_by_customer_id_service() raises exception if addressid not found"""
# def test_get_address_by_customer_id_service_invalid_input(monkeypatch)
"""tests if get_address_by_customer_id_service() raises exception if given invalid input"""

# def test_create_address_service_success(monkeypatch)
"""tests if create_address_service() creates address given valid input"""
# def test_create_address_service_invalid_input(monkeypatch)
"""tests if create_address_service() raises exception given invalid data"""
# def test_create_address_service_partial_input(monkeypatch)
"""tests if create_address_service() creates address given valid input without optional fields"""

# def test_update_address_service_success(monkeypatch)
"""tests if update_address_service() creates address given valid input"""
# def test_update_address_service_invalid_input(monkeypatch)
"""tests if update_address_service() raises excpetion if given invalid input"""
# def test_update_address_service_partial_input(monkeypatch)
"""tests if update_address_service() updates address given valid input without optional fields"""

# def test_delete_address_service_success(monkeypatch)
"""tests if delete_address_service() creates address given valid input"""

# def test_delete_address_service_address_not_found(monkeypatch)
"""tests if update_address_service() raises excpetion if given invalid address id input"""