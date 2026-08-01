from fastapi import APIRouter
from app.services.restaurant_service import get_restaurants
from app.services.menu_service import get_menu_by_restaurant

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


@router.get("")
def restaurants():
    return get_restaurants()


@router.get("/{restaurant_id}/menu")
def menu(restaurant_id: int):
    return get_menu_by_restaurant(restaurant_id)