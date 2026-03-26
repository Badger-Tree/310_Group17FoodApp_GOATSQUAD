from fastapi import APIRouter, Header
from app.schemas.StaffAssignment import StaffAssignmentCreate, StaffAssignmentResponse, StaffAssignmentUpdate
from app.services.staff_assignment_service import assign_staff, update_staff_assignment, remove_staff_assignment
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
