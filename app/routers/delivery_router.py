from app.schemas.Order import OrderResponse
from fastapi import APIRouter, status
from app.schemas.Delivery import DeliveryResponse
from app.services.Delivery_service import (
    assign_delivery_to_courier,
    pickup_delivery,
    complete_delivery,
    cancel_delivery
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

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

@router.delete("/cancel/{delivery_id}", status_code = status.HTTP_200_OK)
def cancel_delivery_route(delivery_id: str):
    """Cancels a delivery."""
    return cancel_delivery(delivery_id)

#No create delivery router because it is part of the create order workflow