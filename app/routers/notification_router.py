from fastapi import APIRouter, status
from typing import List
from app.schemas.notification import Notification
from app.services.notification_service import (notify_order_placed, notify_order_ready_for_pickup, notify_out_for_delivery, notify_order_delivered, notify_payment_status, notify_order_status_update, notify_order_status_update_customer_cancels, notify_refund_issued, get_user_inbox)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/user/{user_id}", response_model=List[Notification])
def get_notifications_by_user(user_id: str):
    """Endpoint to get all notifications for a specific user."""
    return get_user_inbox(user_id)

@router.post("/order-placed", status_code=status.HTTP_201_CREATED)
def notify_order_placed_endpoint(customer_id: str, restaurant_id: str, order_id: str):
    """Endpoint to notify both customer and restaurant when order is placed."""
    notify_order_placed(customer_id, restaurant_id, order_id)
    return {"status": "success", "message": f"Notifications sent for order {order_id}."}

@router.post("/order-ready-for-pickup")
def notify_order_ready_for_pickup_endpoint(courier_id: str, order_id: str):
    """Endpoint to notify the courier when order is ready for pickup."""
    notify_order_ready_for_pickup(courier_id, order_id)
    return {"status": "success", "message": f"Notification sent to courier for order {order_id}."}

@router.post("/out-for-delivery")
def notify_out_for_delivery_endpoint(customer_id: str, order_id: str):
    """Endpoint to notify the customer when order is out for delivery."""
    notify_out_for_delivery(customer_id, order_id)
    return {"status": "success", "message": f"Notification sent to customer for order {order_id}. Out for delivery!"}

@router.post("/order-delivered")
def notify_order_delivered_endpoint(customer_id: str, order_id: str):
    """Endpoint to notify the customer when order is delivered."""
    notify_order_delivered(customer_id, order_id)
    return {"status": "success", "message": f"Notification sent to customer for order {order_id}. Order delivered!"}

@router.post("/payment-status")
def notify_payment_status_endpoint(customer_id: str, order_id: str, is_success: bool):
    """Endpoint to notify the customer whether their payment was successful or failed."""
    notify_payment_status(customer_id, order_id, is_success)
    return {"status": "success", "message": f"Notification sent to customer about payment for order {order_id}."}

@router.post("/order-status-update")
def notify_order_status_update_endpoint(customer_id: str, order_id: str, is_approved: bool):
    """Endpoint to notify the customer when restaurant approves or rejects the order."""
    notify_order_status_update(customer_id, order_id, is_approved)
    return {"status": "success", "message": f"Notification sent to customer for order {order_id}. Order status updated!"}

@router.post("/customer-cancels")
def notify_customer_cancels(restaurant_id: str, order_id: str):
    """Endpoint to notify the restaurant when customer cancels the order."""
    notify_order_status_update_customer_cancels(restaurant_id, order_id)
    return {"status": "success", "message": f"Notification sent to restaurant for order {order_id}. Customer canceled order!"}

@router.post("/refund-issued")
def notify_refund_issued_endpoint(customer_id: str, order_id: str):
    """Endpoint to notify the customer that a refund has been issued for their canceled order."""
    notify_refund_issued(customer_id, order_id)
    return {"status": "success", "message": f"Notification sent to customer for order {order_id}. Refund issued!"}