from fastapi import APIRouter, Header
from app.schemas.Role import UserRole
from app.schemas.StaffAssignment import StaffAssignmentCreate, StaffAssignmentResponse, StaffAssignmentUpdate
from app.services.authorization_service import require_role_service
from app.services.staff_assignment_service import assign_staff, get_staff_assignment_restaurant_service, get_staff_assignment_service, update_staff_assignment, remove_staff_assignment
from app.services.session_manager_service import get_user_from_session
from app.schemas.Token import Token

router = APIRouter(prefix="/staff-assignments", tags=["staff-assignments"])

#Assign a user to a restaurant router
@router.post("/assign_staff", response_model=StaffAssignmentResponse, status_code=201)
def assign_staff_router(staff_assignment: StaffAssignmentCreate, token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    return assign_staff(current_user, str(staff_assignment.staff_id), staff_assignment.assignment)

#Update a staff assignment router
@router.put("/update_staff/{staff_id}", response_model=StaffAssignmentResponse)
def update_staff_assignment_router(staff_id: str, staff_assignment_update: StaffAssignmentUpdate, token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    return update_staff_assignment(current_user, staff_id, staff_assignment_update.assignment)

#Deleting a staff assignment
@router.delete("/remove_staff/{staff_id}", response_model=StaffAssignmentResponse)
def remove_staff_assignment_router(staff_id: str, token: str = Header(...)):
    session = Token(token=token)
    current_user = get_user_from_session(session)
    return remove_staff_assignment(current_user, staff_id)

@router.get("/staff/{user_id}")
def get_staff_assignment(token: str = Header(...)):
    """gets a user's assignments"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    return (get_staff_assignment_service(current_user.id))

@router.get("/restaurant/{restaurant_id}")
def get_staff_assignment_restaurant(restaurant_id: int, token: str = Header(...)):
    """gets a restaurant's staff assignments"""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_service(current_user, UserRole.STAFF)
    return (get_staff_assignment_restaurant_service(restaurant_id))