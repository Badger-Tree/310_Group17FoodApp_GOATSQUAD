from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from datetime import datetime

client = TestClient(app)

mock_restaurant_stats_list = [
    {
        "restaurant_id": "Burger Barn",
        "order_count": 1
    }, 
    
]

def test_get_stats_for_restaurant_valid(mocker):
    """tests the GET /restaurant/stats return the correct information if there are stats to show"""
    mocker.patch("app.routers.track_items_router",return_value=mock_restaurant_stats_list)
    response = client.get("/stat/restaurant/stats")

    assert response.status_code == 200
    assert response.json()[0]["restaurant_name"] == "Burger Barn"
    assert response.json()[0]["order_count"] == 1


def test_get_stats_for_restaurant_invalid(mocker):
    """tests that GET /restaurant/stats returns 404 if there are no stats to show"""
    mocker.patch("app.routers.track_items_router.get_stats_on_restaurants",return_value=False)
    response = client.get("/stat/restaurant/stats")
    assert response.status_code == 404


