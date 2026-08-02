from fastapi import APIRouter, Depends

from app.utils.auth_dependency import get_current_user

from app.services.analytics_service import get_weekly_analytics

router = APIRouter(

    prefix="/analytics",

    tags=["Analytics"]

)


@router.get("/weekly")

def weekly_analytics(

    current_user=Depends(get_current_user)

):

    return get_weekly_analytics(

        current_user["user_id"]

    )