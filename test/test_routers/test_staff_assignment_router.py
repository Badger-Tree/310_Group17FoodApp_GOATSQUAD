from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from unittest.mock import Mock, patch

client = TestClient(app)


@patch("app.routers.staff_assignment_router.assign_staff")
@patch("app.routers.staff_assignment_router.get_user_from_session")


#ASSIGN STAFF TEST: SUCCESS
def test_assign_staff_success(mock_get_user_from_session, mock_assign_staff):
    mock_get_user_from_session.return_value = Mock(id="33", role="OWNER") #id of the owner
    mock_assign_staff.return_value = {
        "assignment_id": "1",
        "restaurant_id": "1001",
        "staff_id": "2", #this is the staff id being assigned
        "assignment": "COURIER"
    }


    payload = {
        "staff_id": "2", #this is the staff id being assigned
        "assignment": "COURIER"
    }

    response = client.post("/staff-assignments/assign_staff", json=payload, headers={"token": "valid_owner_token"})
    assert response.status_code == 201
    assert response.json()["staff_id"] == "2"
    assert response.json()["assignment"] == "COURIER"

#ASSIGN STAFF TEST: FAILURE - DUPLICATE ASSIGNMENT

@patch("app.routers.staff_assignment_router.assign_staff")
@patch("app.routers.staff_assignment_router.get_user_from_session")
def test_assign_staff_duplicate_assignment(mock_get_user_from_session, mock_assign_staff):
    mock_get_user_from_session.return_value = Mock(id="33", role="OWNER")
    mock_assign_staff.side_effect = HTTPException(
        status_code=400,
        detail="This user already has an assignment for this restaurant."
    )

    payload = {
        "staff_id": "2",
        "assignment": "COURIER"
    }

    response = client.post(
        "/staff-assignments/assign_staff",
        json=payload,
        headers={"token": "valid_owner_token"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "This user already has an assignment for this restaurant."

#UPDATE STAFF TEST: SUCCESS
@patch("app.routers.staff_assignment_router.update_staff_assignment")
@patch("app.routers.staff_assignment_router.get_user_from_session")
def test_update_staff_assignment_success(mock_get_user_from_session, mock_update_staff_assignment):
    mock_get_user_from_session.return_value = Mock(id="33", role="OWNER")
    mock_update_staff_assignment.return_value = {
        "assignment_id": "1",
        "restaurant_id": "1001",
        "staff_id": "2",
        "assignment": "MANAGER"
    }

    payload = {
        "assignment": "MANAGER"
    }

    #payload does not have the staff user id because it is being passed in the URL path (basically taking it from the user)
    response = client.put("/staff-assignments/update_staff/2", json=payload, headers={"token": "valid_owner_token"})

    assert response.status_code == 200
    assert response.json()["staff_id"] == "2"
    assert response.json()["assignment"] == "MANAGER"

#UPDATE STAFF TEST: FAILURE - NOT OWNER
@patch("app.routers.staff_assignment_router.update_staff_assignment")
@patch("app.routers.staff_assignment_router.get_user_from_session")
def test_update_staff_assignment_not_owner(mock_get_user_from_session, mock_update_staff_assignment):
    mock_get_user_from_session.return_value = Mock(id="44", role="STAFF") #not an owner
    mock_update_staff_assignment.side_effect = HTTPException(
        status_code=403,
        detail="Only restaurant owners can update staff assignments."
    )

    payload = {
        "assignment": "MANAGER"
    }

    response = client.put("/staff-assignments/update_staff/2", json=payload, headers={"token": "valid_staff_token"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Only restaurant owners can update staff assignments."

#REMOVE STAFF TEST: SUCCESS
@patch("app.routers.staff_assignment_router.remove_staff_assignment")
@patch("app.routers.staff_assignment_router.get_user_from_session")
def test_remove_staff_assignment_success(mock_get_user_from_session, mock_remove_staff_assignment):
    mock_get_user_from_session.return_value = Mock(id="33", role="OWNER")
    mock_remove_staff_assignment.return_value = {
        "assignment_id": "1",
        "restaurant_id": "1001",
        "staff_id": "2",
        "assignment": "COURIER"
    }

    response = client.delete("/staff-assignments/remove_staff/2", headers={"token": "valid_owner_token"})

    assert response.status_code == 200
    assert response.json()["staff_id"] == "2"
    assert response.json()["assignment"] == "COURIER"

#REMOVE STAFF TEST: FAILURE - NOT OWNER
@patch("app.routers.staff_assignment_router.remove_staff_assignment")
@patch("app.routers.staff_assignment_router.get_user_from_session")
def test_remove_staff_assignment_not_owner(mock_get_user_from_session, mock_remove_staff_assignment):
    mock_get_user_from_session.return_value = Mock(id="44", role="STAFF") #not an owner
    mock_remove_staff_assignment.side_effect = HTTPException(
        status_code=403,
        detail="Only restaurant owners can remove staff assignments."
    )

    response = client.delete("/staff-assignments/remove_staff/2", headers={"token": "valid_staff_token"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Only restaurant owners can remove staff assignments."