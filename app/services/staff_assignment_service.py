from typing import List

from app.repositories.staff_assignment_repo import load_all, save_all
from app.repositories.users_repo_csv import load_all as load_users
from app.repositories.restaurants_repo_csv import load_all as load_restaurants

from typing import Dict, Any
from fastapi import HTTPException

from app.schemas.StaffAssignment import StaffAssignmentResponse


#For when a user creates a restaurant, they will get "OWNER" as their assignment.
def create_staff_assignment_for_owner(restaurant_id: str, staff_id: str, assignment: str) -> Dict[str, Any]:

    staff = load_all()

    for existing_assignment in staff:
        if existing_assignment["restaurant_id"] == restaurant_id and existing_assignment["staff_id"] == staff_id:
            raise HTTPException(status_code=400, detail="This user already has an assignment for this restaurant.")
    
    new_assignment = {
        "assignment_id": str(len(staff) + 1),  # Simple ID generation
        "restaurant_id": str(restaurant_id),
        "staff_id": str(staff_id),
        "assignment": assignment
    }

    staff.append(new_assignment)
    save_all(staff)
    return new_assignment

#give assignment to user for a restaurant
def assign_staff(current_user, staff_id: str, assignment: str) -> Dict[str, Any]:

    #load existing staff assignments, users, and restaurants
    staff = load_all()
    users = load_users()
    restaurants = load_restaurants()

    #Check if the restaurant exists and belongs to the current owner user
    selected_restaurant = None
    for restaurant in restaurants:
        if restaurant["owner_id"] == current_user.id:
            selected_restaurant = restaurant
            break

    if selected_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    


    #Find the user whose assignment will be changed
    target_user = None
    for user in users:
        if user["id"] == staff_id:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    #make sure the user is a staff user
    if target_user["role"] != "STAFF":
        raise HTTPException(status_code=400, detail="User is not a staff member.")

    #Check for duplicate assignments. Cannot have a user with multiple roles
    for existing_assignment in staff:
        if existing_assignment["restaurant_id"] == selected_restaurant["restaurant_id"] and existing_assignment["staff_id"] == staff_id:
            raise HTTPException(status_code=400, detail="This user already has an assignment for this restaurant.")
        
    # Create new assignment
    new_assignment = {
        "assignment_id": str(len(staff) + 1),  # Simple ID generation
        "restaurant_id": str(selected_restaurant["restaurant_id"]),
        "staff_id": staff_id,
        "assignment": assignment
    }
    
    # Save the new assignment
    staff.append(new_assignment)
    save_all(staff)
    
    return new_assignment

#Update a staff's assignment to another assignment for a restaurant
def update_staff_assignment(current_user, staff_id: str, new_assignment: str) -> Dict[str, Any]:
      
    #load existing staff assignments, users, and restaurants
    staff = load_all()
    users = load_users()
    restaurants = load_restaurants()

    #Check if the restaurant exists and check if the current user is the owner
    selected_restaurant = None
    for restaurant in restaurants:
        if restaurant["owner_id"] == current_user.id:
            selected_restaurant = restaurant
            break

    if selected_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found.")



    #Find the user whose assignment will be changed
    target_user = None
    for user in users:
        if user["id"] == staff_id:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    

    
    #Find and update assignment
    assignment_to_update = None

    for existing_assignment in staff:
        if(existing_assignment["restaurant_id"] == str(selected_restaurant["restaurant_id"]) and existing_assignment["staff_id"] == staff_id):
            assignment_to_update = existing_assignment
            break

    if assignment_to_update is None:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    
    assignment_to_update["assignment"] = new_assignment
    save_all(staff)
    
    return assignment_to_update

#remove/return user's assignment to STAFF
def remove_staff_assignment(current_user, staff_id: str) -> Dict[str, Any]:

    #load existing staff assignments, users, and restaurants
    staff = load_all()
    users = load_users()
    restaurants = load_restaurants()


    #Check if the restaurant exists and check if the current user is the owner
    selected_restaurant = None
    for restaurant in restaurants:
        if restaurant["owner_id"] == current_user.id:
            selected_restaurant = restaurant
            break

    if selected_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found.")


    #Find the user whose assignment will be changed
    target_user = None
    for user in users:
        if user["id"] == staff_id:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    # Find and remove the assignment
    assignment_to_remove = None
    
    for existing_assignment in staff:
        if (existing_assignment["restaurant_id"] == str(selected_restaurant["restaurant_id"]) and existing_assignment["staff_id"] == staff_id):
            assignment_to_remove = existing_assignment
            break

    if assignment_to_remove is None:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    
    staff.remove(assignment_to_remove)
    save_all(staff)
    
    return assignment_to_remove

def get_staff_assignment_service(user_id: str) -> List[StaffAssignmentResponse]:
    staff_assignments = load_all()
    assignments = []
    for staff in staff_assignments:
        if staff["staff_id"] == user_id:
            assignments.append(staff)
    return assignments

def get_staff_assignment_restaurant_service(restaurant_id: int) -> List[StaffAssignmentResponse]:
    staff_assignments = load_all()
    assignments = []
    for assignment in staff_assignments:
        if int(assignment["restaurant_id"]) == restaurant_id:
            assignments.append(assignment)
    return assignments