from pathlib import Path
import csv, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.csv"

def load_all() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
       return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
       reader = csv.DictReader(f)
       return list(reader)
   
def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    fields = ["id",
                "email",
                "first_name",
                "last_name",
                "password",
                "role",
                "created_date"]
                
    with tmp.open("w", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
        
    os.replace(tmp, DATA_PATH)
    
def find_by_id_repo(user_id: str) -> dict[str,Any] | None:
    users = load_all()
    for user in users: 
        if user.get("id") == user_id:
            return user
    return None

def find_by_email_repo(email: str) -> dict[str,Any] | None:
    user_data = load_all()
    for user in user_data: 
        if user.get("email").lower() == email.lower():
            return user
    return None

def add_user_repo(user:dict):
    users = load_all()
    if any(u["id"] == user["id"] for u in users):
        raise ValueError("User ID already exists")
    users.append(user)
    save_all(users)
    return user

def update_user_repo(user_id: str, updated_fields:dict) -> dict | None:
    users = load_all()
    for user in users:
        if user["id"] == user_id:
            user.update(updated_fields)
            save_all(users)
            return user
    return None