from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================
# User Profile Response
# ==========================================

class UserProfileResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str

    age: Optional[int] = None
    gender: Optional[str] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None

    goal: Optional[str] = None
    diet_preferences: Optional[str] = None

    daily_budget: Optional[float] = None
    activity_level: Optional[str] = None

    daily_calories: Optional[int] = None
    daily_protein: Optional[int] = None
    daily_carbs: Optional[int] = None
    daily_fat: Optional[int] = None
    daily_fiber: Optional[int] = None

    bmi: Optional[float] = None
    target_weight: Optional[float] = None

    allergies: Optional[str] = None
    health_conditions: Optional[str] = None


# ==========================================
# User Profile Update Request
# ==========================================

class UserProfileUpdate(BaseModel):

    name: Optional[str] = None

    age: Optional[int] = None
    gender: Optional[str] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None

    goal: Optional[str] = None
    diet_preferences: Optional[str] = None

    daily_budget: Optional[float] = None
    activity_level: Optional[str] = None

    target_weight: Optional[float] = None

    allergies: Optional[str] = None
    health_conditions: Optional[str] = None