from ..repositories import favorite_repo
from ..services import restaurant_service, order_service

def add_favorite(user_id: str, target_id: int, favorite_type: str):
    favorites = favorite_repo.load_all()

    for fav in favorites:
        if (fav["user_id"] == user_id and 
            fav["target_id"]== target_id and 
            fav["favorite_type"] == favorite_type):
            return None
        
    new_fav = {
        "user_id": user_id,
        "target_id": target_id,
        "favorite_type": favorite_type
    }

    favorites.append(new_fav)
    favorite_repo.save_all(favorites)
    return new_fav

def get_favorites(user_id: str):
    """returns full restaurant/order info for all favs of user"""
    all_favs = [f for f in favorite_repo.load_all() if f["user_id"] == user_id]
    
    result = []
    for fav in all_favs:
        if fav["favorite_type"] == "RESTAURANT":
            all_restaurants = restaurant_service.sort_restaurants_by_name_service()
            data = next((r for r in all_restaurants if r.restaurant_id == int(fav["target_id"])), None)
        elif fav["favorite_type"] == "ORDER":
            order_id_str = str(fav["target_id"])
            data = order_service.get_order_by_order_id_service(order_id_str)

        if data:
            result.append(data)

    return result

def delete_favorite(user_id: str, target_id: str, favorite_type: str):
    """removes favorite from csv. if fav doesnt exist, does nothing"""
    favorites = favorite_repo.load_all()
    initial_count = len(favorites)

    updated_favorites = [
        f for f in favorites
        if not (str(f["user_id"]) == str(user_id) and
                str(f["target_id"]) == str(target_id) and
                str(f["favorite_type"]).upper().strip() == str(favorite_type).upper().strip())
    ]
    if len(updated_favorites) == initial_count:
        return False
    
    favorite_repo.save_all(updated_favorites)
    return True