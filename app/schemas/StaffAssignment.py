from pydantic import BaseModel
from typing import Optional


"""Staff base model"""
class StaffAssignmentBase(BaseModel):
    restaurant_id: int
    user_id: int #The person being assigned a role by the manager
    role: str

"""Staff Assignment Constructor"""
class StaffAssignmentCreate(StaffAssignmentBase):
    assigned_by: int #temporary authentication. This will ask for the user id of the manager doing the assigning

"""Update the role"""
class StaffAssignmentUpdate(BaseModel):
    role: Optional[str] = None

"""Returns the assignment id and who it was assigned by"""
class StaffAssignmentResponse(StaffAssignmentBase):
    assignment_id: int
    assigned_by: int

