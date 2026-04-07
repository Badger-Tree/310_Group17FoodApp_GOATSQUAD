from unittest.mock import patch, Mock
from app.services.staff_assignment_service import assign_staff, update_staff_assignment, remove_staff_assignment, get_staff_assignment_service, get_staff_assignment_restaurant_service
import pytest
from fastapi import HTTPException

@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")

#ASSIGN STAFF TEST: SUCCESS
def test_assign_staff_success(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):

    current_user = Mock(id="33", role="OWNER") #id of the owner

    mock_load_all.return_value = []
    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]
    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "33"}
    ]

    result= assign_staff(current_user, "2", "COURIER")

    assert result["staff_id"] == "2"
    assert result["assignment"] == "COURIER"
    mock_save_all.assert_called_once()

#ASSIGN STAFF TEST: FAILURE - DUPLICATE ASSIGNMENT
@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")
def test_assign_staff_duplicate_assignment(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):
    
    current_user = Mock(id="33", role="OWNER")

    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]

    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "33"}
    ]

    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        }
    ]

    with pytest.raises(HTTPException) as exc_info:
        assign_staff(current_user, "2", "COURIER")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "This user already has an assignment for this restaurant."

#UPDATE ASSIGNMENT TEST: SUCCESS
@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")
def test_update_staff_assignment_success(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):
    current_user = Mock(id="33", role="OWNER")

    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]

    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "33"}
    ]

    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        }
    ]

    result = update_staff_assignment(current_user, "2", "CHEF")

    assert result["staff_id"] == "2"
    assert result["assignment"] == "CHEF"
    mock_save_all.assert_called_once()

#UPDATEA ASSIGNMENT TEST: FAILURE - NOT OWNER
@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")
def test_update_staff_assignment_not_owner(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):
    current_user = Mock(id="33", role="STAFF")

    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]

    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "44"}
    ]

    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        }
    ]

    with pytest.raises(HTTPException) as exc_info:
        update_staff_assignment(current_user, "2", "CHEF")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant not found."

#REMOVE STAFF ASSIGNMENT: SUCCESS
@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")
def test_remove_staff_assignment_success(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):
    current_user = Mock(id="33", role="OWNER")

    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]

    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "33"}
    ]

    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        }
    ]

    result = remove_staff_assignment(current_user, "2")

    assert result["staff_id"] == "2"
    assert result["assignment"] == "COURIER"
    mock_save_all.assert_called_once()

#REMOVE STAFF ASSIGNMENT: FAILURE - NO STAFF ASSIGNMENT
@patch("app.services.staff_assignment_service.save_all")
@patch("app.services.staff_assignment_service.load_all")
@patch("app.services.staff_assignment_service.load_restaurants")
@patch("app.services.staff_assignment_service.load_users")
def test_remove_staff_assignment_no_assignment(mock_load_users, mock_load_restaurants, mock_load_all, mock_save_all):
    current_user = Mock(id="33", role="OWNER")

    mock_load_users.return_value = [
        {"id": "2", "role": "STAFF"}
    ]

    mock_load_restaurants.return_value = [
        {"restaurant_id": "1001", "owner_id": "33"}
    ]

    mock_load_all.return_value = [] #no existing staff assignments

    with pytest.raises(HTTPException) as exc_info:
        remove_staff_assignment(current_user, "2")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Assignment not found."


#GET STAFF ASSIGNMENT BY USER ID - SUCCESS
@patch("app.services.staff_assignment_service.load_all")
def test_get_staff_assignment_by_user_id_success(mock_load_all):
    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        },
        {
            "assignment_id": "2",
            "restaurant_id": "1002",
            "staff_id": "2",
            "assignment": "CHEF"
        },
        {
            "assignment_id": "3",
            "restaurant_id": "1003",
            "staff_id": "5",
            "assignment": "CASHIER"
        }
    ]

    result = get_staff_assignment_service("2")

    result = get_staff_assignment_service("2")

    assert len(result) == 2
    assert result[0]["staff_id"] == "2"
    assert result[0]["assignment"] == "COURIER"
    assert result[1]["staff_id"] == "2"
    assert result[1]["assignment"] == "CHEF"

#GET STAFF ASSIGNMENT BY USER ID - FAILURE 
@patch("app.services.staff_assignment_service.load_all")
def test_get_staff_assignment_service_not_found(mock_load_all):
    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        }
    ]

    result = get_staff_assignment_service("99")

    assert result == []

#GET STAFF ASSIGNMENT BY RESTAURANT ID - SUCCESS 
@patch("app.services.staff_assignment_service.load_all")
def test_get_staff_assignment_restaurant_service_success(mock_load_all):
    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        },
        {
            "assignment_id": "2",
            "restaurant_id": "1001",
            "staff_id": "3",
            "assignment": "CHEF"
        },
        {
            "assignment_id": "3",
            "restaurant_id": "1002",
            "staff_id": "4",
            "assignment": "CASHIER"
        }
    ]

    result = get_staff_assignment_restaurant_service(1001)

    assert len(result) == 2
    assert result[0]["restaurant_id"] == "1001"
    assert result[0]["staff_id"] == "2"
    assert result[0]["assignment"] == "COURIER"

    assert result[1]["restaurant_id"] == "1001"
    assert result[1]["staff_id"] == "3"
    assert result[1]["assignment"] == "CHEF"

#GET STAFF ASSIGNMENT BY RESTAURANT ID - FAILURE
@patch("app.services.staff_assignment_service.load_all")
def test_get_staff_assignment_restaurant_service_not_found(mock_load_all):
    mock_load_all.return_value = [
        {
            "assignment_id": "1",
            "restaurant_id": "1001",
            "staff_id": "2",
            "assignment": "COURIER"
        },
        {
            "assignment_id": "2",
            "restaurant_id": "1002",
            "staff_id": "3",
            "assignment": "CHEF"
        }
    ]

    result = get_staff_assignment_restaurant_service(9999)

    assert result == []
