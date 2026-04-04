from app.schemas.favorite import FavoriteCreate
import pytest
from pydantic import ValidationError

def test_favorite_schema_invalid_type():
    with pytest.raises(ValidationError):
        FavoriteCreate(target_id="123", favorite_type="INVALID_TYPE")

def test_favorite_create_success():
    fav = FavoriteCreate(target_id="123", favorite_type="RESTAURANT")
    assert fav.target_id == "123"
    assert fav.favorite_type == "RESTAURANT"