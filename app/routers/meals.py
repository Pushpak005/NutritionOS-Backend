from fastapi import APIRouter, Depends

from app.utils.auth_dependency import get_current_user
from app.services.meal_service import log_meal

router = APIRouter(
    prefix="/meals",
    tags=["Meals"]
)


@router.post("/log")
def create_meal(
    menu_item_id: int,
    meal_type: str,
    quantity: int,
    current_user=Depends(get_current_user)
):

    return log_meal(
        current_user["user_id"],
        menu_item_id,
        meal_type,
        quantity
    )