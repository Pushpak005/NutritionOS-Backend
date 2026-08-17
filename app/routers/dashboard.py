from fastapi import APIRouter, Depends
from app.utils.auth_dependency import get_current_user
from app.services.dashboard_service import get_dashboard


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(current_user=Depends(get_current_user)):

    return get_dashboard(
        current_user["user_id"]
    )