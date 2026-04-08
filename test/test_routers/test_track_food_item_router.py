from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

mock_food_item_stats_list = [
    {
        "food_item_id": 1,
        "food_name": "name",
        "order_count": 1
    }, 
    
]

def test_get_stats_for_food_item_valid(mocker):
    """tests the GET /food_items/{restaurant_id}/stats return the correct information if there are stats to show"""
    mocker.patch("app.routers.track_food_items_router.get_stats_on_food",return_value=mock_food_item_stats_list)
    response = client.get("/food_stat/food_items/1/stats")

    assert response.status_code == 200
    assert response.json()[0]["food_item_id"] == 1
    assert response.json()[0]["food_name"] == "name"
    assert response.json()[0]["order_count"] == 1


def test_get_stats_for_food_item_invalid(mocker):
    """tests that GET /food_items/{restaurant_id}/stats returns 404 if there are no stats to show"""
    mocker.patch("app.routers.track_food_items_router.get_stats_on_food",return_value=False)
    response = client.get("/food_stat/food_items/999/stats")
    assert response.status_code == 404