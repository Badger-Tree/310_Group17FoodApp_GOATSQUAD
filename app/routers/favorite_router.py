from fastapi import APIRouter, Depends, Header, HTTPException
from app.services import favorite_service
from app.services.session_manager_service import get_user_from_session
from app.schemas.Token import Token
from app.schemas.favorite import FavoriteType

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/me")
def list_my_favorites(token: str = Header(...)):
    """uses session manager to get user info from token then returns full restaurant/order info for all favs of user"""
    session_token = Token(token=token)
    current_user = get_user_from_session(session_token)
    return favorite_service.get_favorites(current_user.id)

@router.post("/{fav_type}/{target_id}", status_code=201)
def add_to_favorites(fav_type: FavoriteType, target_id: str, token: str = Header(...)):
    """adds a restaurant or order to user's favorites. fav_type is either RESTAURANT or ORDER, target_id is restaurant id or order id depending on fav_type."""

    user = get_user_from_session(Token(token=token))
    result = favorite_service.add_favorite(user.id, target_id, fav_type)
    if not result:
        raise HTTPException(status_code=400, detail= "Already in favorites")
    return result

@router.delete("/{fav_type}/{target_id}", status_code=204)
def remove_favorite(fav_type: FavoriteType, target_id: str, token: str = Header(...)):
    """removes restaurant or order from user's favorites. target_id is restaurant id or order id depending on fav_type."""
    
    user = get_user_from_session(Token(token=token))
    success = favorite_service.delete_favorite(user.id, target_id, fav_type.value)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return None

