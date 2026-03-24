from app.repositories.staff_assignment_repo import load_all, save_all
from app.repositories.users_repo_csv import load_all as load_users
from app.repositories.restaurants_repo_csv import load_all as load_restaurants

from typing import Dict, Any
from fastapi import HTTPException

#assign staff role to user for a restaurant
def assign_staff_role(current_user, restaurant_id: int, staff_user_id: str, role: str) -> Dict[str, Any]:

    #check if the current user is either owner
    if current_user.role != "OWNER":
        raise HTTPException(status_code=403, detail="Only restaurant owners and managers can assign staff roles.")
    
    #load existing staff assignments, users, and restaurants
    staff = load_all()
    users = load_users()
    restaurants = load_restaurants()

    #Find the user whose role will be changed
    target_user = None
    for user in users:
        if user["id"] == staff_user_id:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    #make sure the user is a staff user
    if target_user["role"] != "STAFF":
        raise HTTPException(status_code=400, detail="User is not a staff member.")


    #Check if the restaurant exists
    selected_restaurant = None
    for restaurant in restaurants:
        if int(restaurant["restaurant_id"]) == restaurant_id:
            selected_restaurant = restaurant
            break

    if selected_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
    
    #make sure the current user is the owner of the restaurant
    if selected_restaurant["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only the restaurant owner can assign staff roles.")

    #Check for duplicate assignments. Cannot have a user with multiple roles
    for assignment in staff:
        if assignment["restaurant_id"] == str(restaurant_id) and assignment["user_id"] == staff_user_id:
            raise HTTPException(status_code=400, detail="This user already has a role assigned for this restaurant.")
        
    # Create new assignment
    new_assignment = {
        "assignment_id": str(len(staff) + 1),  # Simple ID generation
        "restaurant_id": str(restaurant_id),
        "user_id": staff_user_id,
        "role": role
    }
    
    # Save the new assignment
    staff.append(new_assignment)
    save_all(staff)
    
    return new_assignment