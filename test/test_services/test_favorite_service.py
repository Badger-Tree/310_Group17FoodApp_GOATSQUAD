import pytest
from unittest.mock import patch
from app.services import favorite_service

mock_favorites = [
    {"user_id": "1", "target_id": "101", "favorite_type": "RESTAURANT"},
    {"user_id": "1", "target_id": "202", "favorite_type": "ORDER"},
]

def test_add_favorite_success():
    with patch("app.repositories.favorite_repo.load_all", return_value=mock_favorites):
        with patch("app.repositories.favorite_repo.save_all") as mock_save:
            result = favorite_service.add_favorite("1", "303", "RESTAURANT")
            assert result == {"user_id": "1", "target_id": "303", "favorite_type": "RESTAURANT"}
            mock_save.assert_called_once()

def test_delete_favorite_success():
    with patch("app.repositories.favorite_repo.load_all", return_value=mock_favorites):
        with patch("app.repositories.favorite_repo.save_all") as mock_save:
            result = favorite_service.delete_favorite("1", "101", "RESTAURANT")
            assert result == True
            mock_save.assert_called_once()