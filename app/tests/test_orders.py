from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_success():
    # here I want to input data that I know will pass
    pass
    
# def test_create_order_fail()