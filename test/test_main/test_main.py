from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_read_health():
    """tests that health() is returning ok response"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_main():
    """tests that main is correctly connecting to root"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GoatSquad is Live!"}