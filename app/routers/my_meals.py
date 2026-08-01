from fastapi import APIRouter, Depends

from app.utils.auth_dependency import get_current_user
from app.services.my_meals_service import get_my_meals

router = APIRouter(
    prefix="/my-meals",
    tags=["My Meals"]
)


@router.get("")
def my_meals(current_user=Depends(get_current_user)):

    return get_my_meals(
        current_user["user_id"]
    )