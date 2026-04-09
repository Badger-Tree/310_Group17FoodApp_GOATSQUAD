from app.schemas.Order import OrderResponse
from fastapi import APIRouter, Header, status
from app.schemas.Delivery import DeliveryResponse
from app.schemas.Token import Token
from app.services.session_manager_service import get_user_from_session
from app.services.Delivery_service import (
    assign_delivery_to_courier,
    get_orders_assigned_to_courier,
    pickup_delivery,
    complete_delivery,
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.get("/my-orders", response_model=list[OrderResponse], status_code=status.HTTP_200_OK)
def get_my_assigned_orders(token: str = Header(...)):
    """Returns orders assigned to the currently logged-in courier."""
    session = Token(token=token)
    current_user = get_user_from_session(session)
    return get_orders_assigned_to_courier(current_user.id)

@router.put("/assign/{delivery_id}/{courier_id}", response_model=DeliveryResponse, status_code = status.HTTP_200_OK)
def assign_delivery(delivery_id: str, courier_id: str):
    """Assigns a delivery to a courier."""
    return assign_delivery_to_courier(delivery_id, courier_id)

@router.put("/pickup/{delivery_id}", response_model=OrderResponse, status_code = status.HTTP_200_OK)
def pickup_delivery_route(delivery_id: str):
    """Marks a delivery as picked up."""
    return pickup_delivery(delivery_id)

@router.put("/complete/{delivery_id}", response_model=OrderResponse, status_code = status.HTTP_200_OK)
def complete_delivery_route(delivery_id: str):
    """Marks a delivery as complete."""
    return complete_delivery(delivery_id)



#No create delivery router because it is part of the create order workflow
