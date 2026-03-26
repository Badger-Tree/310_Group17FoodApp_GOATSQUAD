from pydantic import BaseModel
from typing import Optional


"""Staff base model"""
class StaffAssignmentBase(BaseModel):
    staff_id: str #The owner assigning the roles
    assignment: str

"""Create the assignment"""
class StaffAssignmentCreate(StaffAssignmentBase):
    pass

"""Update the assignment"""
class StaffAssignmentUpdate(BaseModel):
    assignment: Optional[str] = None

"""Returns the assignment id and who it was assigned by"""
class StaffAssignmentResponse(StaffAssignmentBase):
    assignment_id: str
    restaurant_id: str
    staff_id: str
    assignment: str


