from fastapi import APIRouter, status
from app.schemas.Delivery import DeliveryResponse
from app.services.Delivery_service import (
    assign_delivery_to_courier,
    update_delivery_status,
    cancel_delivery
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.put("/assign/{delivery_id}/{courier_id}", response_model=DeliveryResponse, status_code = status.HTTP_200_OK)
def assign_delivery(delivery_id: str, courier_id: str):
    """Assigns a delivery to a courier."""
    return assign_delivery_to_courier(delivery_id, courier_id)

@router.put("/status/{delivery_id}/{new_status}", response_model=DeliveryResponse, status_code = status.HTTP_200_OK)
def update_delivery_status(delivery_id: str, new_status: str):
    """Updates the delivery status of an order."""
    return update_delivery_status(delivery_id, new_status)

@router.put("/cancel/{delivery_id}", response_model=DeliveryResponse, status_code = status.HTTP_200_OK)
def cancel_delivery(delivery_id: str):
    """Cancels a delivery."""
    return cancel_delivery(delivery_id)

#No create delivery router because it is part of the create order workflow