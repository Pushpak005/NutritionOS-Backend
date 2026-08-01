from fastapi import APIRouter, Depends

from app.utils.auth_dependency import get_current_user

from app.services.ai_service import recommend_meals

router = APIRouter(

    prefix="/ai",

    tags=["AI"]

)


@router.get("/recommend")

def ai_recommend(

    current_user=Depends(get_current_user)

):

    return recommend_meals(

        current_user["user_id"]

    )