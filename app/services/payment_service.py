import random


def process_payment_service(amount: float) -> bool:
    """This simulates a payment and returns a boolean to indicate if payment was successful. 20% of payments will be false."""
    return random.choice([True, True, True, True,False])
    
def process_refund_service(amount: float) -> bool:
    """This simulates a refund and returns a boolean to indicate if refund was successful. 20% of payments will be false."""
    return random.choice([True, True, True, True,False])