from fastapi import APIRouter, HTTPException, Header
from ..schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from ..services import inventory_service
from ..schemas.Token import Token
from ..services.session_manager_service import get_user_from_session
from ..services.authorization_service import require_role_service
from ..schemas.Role import UserRole

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/{food_item_id}", response_model=Inventory)
def get_inventory(food_item_id: int, token: str = Header(...)):
    """Get inventory record by food item ID."""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_service(current_user, UserRole.STAFF)
    record = inventory_service.get_inventory_by_food_id(food_item_id)
    if not record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return record

@router.post("/", response_model=Inventory)
def create_inventory(payload: InventoryCreate, token: str = Header(...)):
    """Create a new inventory record."""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_service(current_user, UserRole.STAFF)
    return inventory_service.create_inventory_record(payload)

@router.patch("/{food_item_id}", response_model=Inventory)
def update_inventory(food_item_id: int, payload: InventoryUpdate, token: str = Header(...)):
    """Update an existing inventory record."""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    require_role_service(current_user, UserRole.STAFF)
    updated_record = inventory_service.update_inventory(food_item_id, payload.quantity)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_record
