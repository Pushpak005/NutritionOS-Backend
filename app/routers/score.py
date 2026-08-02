from fastapi import APIRouter, Depends

from app.utils.auth_dependency import get_current_user

from app.services.score_service import calculate_score


router = APIRouter(

    prefix="/score",

    tags=["Nutrition Score"]

)


@router.get("/today")

def today_score(

    current_user=Depends(get_current_user)

):

    return calculate_score(

        current_user["user_id"]

    )