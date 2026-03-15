from app.repositories import notification_repo

def notify_order_placed(customer_id: str, restaurant_id: str, order_id: str):
    """Sends a notification to the customer and restaurant owner when order is submitted."""
    notification_repo.create_notification({
        "recipient_user_id": customer_id,
        "notification_type": "order",
        "message": f"Order {order_id} placed! We'll let you know when it's ready.",
        "status": "pending"
    })

    notification_repo.create_notification({
        "recipient_user_id": restaurant_id,
        "notification_type": "order",
        "message": f"New order received: {order_id}. Please begin preparation.",
        "status": "pending"
    })

def notify_order_ready_for_pickup(courier_id: str, order_id: str):
    """Sends a notification to the courier when an order is ready for pickup."""
    notification_repo.create_notification({
        "recipient_user_id": courier_id,
        "notification_type": "delivery",
        "message": f"Order {order_id} is ready for pickup at the restaurant.",
        "status": "pending"
    })

def notify_out_for_delivery(customer_id: str, order_id: str):
    """Called when the courier picks up the order; sends notification to customer."""
    notification_repo.create_notification({
        "recipient_user_id": customer_id,
        "notification_type": "delivery",
        "message": f"Order {order_id} is on the way! Your courier is nearby.",
        "status": "pending"
    })

def notify_order_delivered(customer_id: str, order_id: str):
    """When courier completes drop-off, notifies customer"""
    notification_repo.create_notification({
        "recipient_user_id": customer_id,
        "notification_type": "delivery",
        "message": f"Order {order_id} has been delivered. Enjoy your meal!",
        "status": "delivered"
    })

def notify_payment_status(customer_id: str, order_id: str, is_success: bool):
    """Notifies customer whether their payment went through or failed."""
    if is_success:
        message = f"Payment for order {order_id} was successful. The restaurant is preparing your meal!"
        status = "pending"
    else:
        message = f"Payment for order {order_id} failed. Please update your payment information and try again."
        status = "failed"

    notification_repo.create_notification({
        "recipient_user_id": customer_id,
        "notification_type": "payment",
        "message": message,
        "status": status
    })

def notify_order_status_update(customer_id: str, order_id: str, is_approved: bool):
    """Notifies customer when restaurant approves or rejects the order."""
    if is_approved:
        message = f"Your order {order_id} has been approved by the restaurant. We'll let you know when it's ready!"
        status = "pending"
    else:
        message = f"Unfortunately, your order {order_id} was canceled by the restaurant."
        status = "failed"

    notification_repo.create_notification({
        "recipient_user_id": customer_id,
        "notification_type": "order",
        "message": message,
        "status": status
    })