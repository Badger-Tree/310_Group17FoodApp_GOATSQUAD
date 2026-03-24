import uuid
from datetime import datetime, timezone
from app.repositories.deliveries_repo_csv import load_all, save_all
from app.repositories.orders_repo import load_all as load_orders
from app.repositories.staff_assignment_repo import load_all as load_staff_assignments
from app.schemas.Delivery import DeliveryResponse
from fastapi import HTTPException

#Create delivery service, takes in order object
def create_delivery_service(order: dict) -> DeliveryResponse:
    """Creates a delivery record for the given order and returns the delivery details."""
    deliveries = load_all()

    new_delivery = {
        "order_id": order["order_id"],
        "courier_id": None, #Courier will be assigned later on
        "created_date": datetime.now(timezone.utc).isoformat(),
        "address_id": order["delivery_address_id"],
        "delivery_status": "PENDING",
        "delivery_id": str(uuid.uuid4())
    }

    deliveries.append(new_delivery)
    save_all(deliveries)

    return DeliveryResponse(**new_delivery)

#Assigning a delivery to a courier
def assign_delivery_to_courier(delivery_id: str, courier_id: str) -> DeliveryResponse:
    """Assigns a delivery to a courier and updates the delivery status."""
    deliveries = load_all()
    orders = load_orders()
    staff_assignments = load_staff_assignments()

    #Get the right delivery record
    target_delivery = None
    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            target_delivery = delivery
            break
    
    if target_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    #Get the right order
    target_order = None
    for order in orders:
        if order["order_id"] == target_delivery["order_id"]:
            target_order = order
            break

    if target_order is None:
        raise HTTPException(status_code=404, detail="Order not found for delivery")
    
    #Get a valid courier
    valid_courier = None
    for assignment in staff_assignments:
        if (
            assignment["user_id"] == courier_id
            and assignment["restaurant_id"] == str(target_order["restaurant_id"])
            and assignment["role"] == "COURIER"
        ):
            valid_courier = assignment
            break

    if valid_courier is None:
        raise HTTPException(status_code=400, detail="Invalid courier assignment")
    
    target_delivery["courier_id"] = courier_id
    target_delivery["delivery_status"] = "ASSIGNED"

    save_all(deliveries)
    return DeliveryResponse(**target_delivery)

#Service to update delivery status
def update_delivery_status(delivery_id: str, new_status: str) -> DeliveryResponse:
    """Update the delivery status"""
    deliveries = load_all()
    target_delivery = None
    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            target_delivery = delivery
            break
    
    if target_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    target_delivery["delivery_status"] = new_status

    save_all(deliveries)
    return DeliveryResponse(**target_delivery)

#Service to cancel a delivery
def cancel_delivery(delivery_id: str) -> DeliveryResponse:
    """Cancel a delivery by updating its status to 'CANCELED'."""
    
    return update_delivery_status(delivery_id, "CANCELED")
