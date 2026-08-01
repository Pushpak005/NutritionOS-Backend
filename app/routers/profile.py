from fastapi import APIRouter, Depends, HTTPException

from app.utils.auth_dependency import get_current_user
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.profile_service import get_profile, update_profile

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("", response_model=ProfileResponse)
def read_profile(current_user=Depends(get_current_user)):

    profile = get_profile(current_user["user_id"])

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.put("", response_model=ProfileResponse)
def edit_profile(
    profile: ProfileUpdate,
    current_user=Depends(get_current_user)
):

    updated_profile = update_profile(
        current_user["user_id"],
        profile.model_dump()
    )

    return updated_profile