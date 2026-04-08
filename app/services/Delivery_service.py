import uuid
from datetime import datetime, timezone
from app.repositories.deliveries_repo_csv import load_all, save_all
from app.repositories.orders_repo import load_all as load_orders
from app.repositories.order_items_repo import load_all as load_order_items
from app.repositories.staff_assignment_repo import load_all as load_staff_assignments
from app.schemas.Delivery import DeliveryResponse
from app.schemas.OrderStatus import OrderStatus
from app.schemas.Order import OrderResponse
from app.schemas.OrderItem import OrderItemResponse
# from app.services.order_service import set_order_status_service
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
        "delivery_id": str(uuid.uuid4())
    }

    deliveries.append(new_delivery)
    save_all(deliveries)

    return DeliveryResponse(**new_delivery)

#Assigning a delivery to a courier
def assign_delivery_to_courier(delivery_id: str, courier_id: str) -> DeliveryResponse:
    """Assigns a delivery to a courier"""
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
            assignment["staff_id"] == courier_id #fixed bug here
            and assignment["restaurant_id"] == str(target_order["restaurant_id"])
            and assignment["assignment"] == "COURIER"
        ):
            valid_courier = assignment
            break

    if valid_courier is None:
        raise HTTPException(status_code=400, detail="Invalid courier assignment")
    
    target_delivery["courier_id"] = courier_id

    save_all(deliveries)
    return DeliveryResponse(**target_delivery)

def get_orders_assigned_to_courier(courier_id: str) -> list[OrderResponse]:
    """Returns orders whose delivery has been assigned to the given courier."""
    deliveries = load_all()
    orders = load_orders()
    order_items = load_order_items()

    courier_delivery_ids = {
        delivery["delivery_id"]: delivery
        for delivery in deliveries
        if delivery.get("courier_id") == courier_id
    }

    assigned_orders = []
    for order in orders:
        if order.get("delivery_id") not in courier_delivery_ids:
            continue

        items_response = []
        for item in order_items:
            if item.get("order_id") == order.get("order_id"):
                items_response.append(OrderItemResponse(**item))

        assigned_orders.append(OrderResponse(**order, items=items_response))

    return assigned_orders

#SET DELIVERY AS PICKED UP
def pickup_delivery(delivery_id: str):
    from app.services.order_service import set_order_status_service
    deliveries = load_all()

    target_delivery = None
    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            target_delivery = delivery
            break
    
    if target_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    return set_order_status_service(target_delivery["order_id"], OrderStatus.OUT_FOR_DELIVERY)

#SET DELIVERY AS COMPLETE
def complete_delivery(delivery_id: str):
    from app.services.order_service import set_order_status_service
    deliveries = load_all()

    target_delivery = None
    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            target_delivery = delivery
            break
    
    if target_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    return set_order_status_service(target_delivery["order_id"], OrderStatus.COMPLETED)
