import random
from app.services.payment_service import process_payment_service, process_refund_service


def test_process_payment_service_success(mocker):
    """Tests that process_payment_service will output True if it generates a successful payment"""
    mocker.patch("app.services.payment_service.random.choice", return_value = True)   
    result = process_payment_service(111.25)
    assert result is True

    
def test_process_payment_service_payment_unsuccessful(mocker):
    """Tests that process_payment_service will output False if it generates a failed payment"""
    mocker.patch("app.services.payment_service.random.choice", return_value = False)  
    result = process_payment_service(111.25)
    assert result == False
    

def test_process_refund_service_success(mocker):
    """Tests that process_refund_service will output True if it generates a successful payment"""
    mocker.patch("app.services.payment_service.random.choice", return_value = True)   
    result = process_refund_service(111.25)
    assert result == True
    
    
def test_process_refund_service_unsuccessful(mocker):
    """Tests that process_refund_service will output False if it generates a failed payment"""
    mocker.patch("app.services.payment_service.random.choice", return_value = False)
    result = process_refund_service(111.25)
    assert result == False
    

