from pydantic import BaseModel
from typing import Optional


class ProfileResponse(BaseModel):

    id: int

    name: str

    email: str

    age: int

    gender: str

    height_cm: float

    weight_kg: float

    goal: str

    activity_level: str

    daily_budget: float

    diet_preferences: str

    # -------------------------
    # Nutrition Engine
    # -------------------------

    bmi: Optional[float] = None

    daily_calories: Optional[int] = None

    daily_protein: Optional[int] = None

    daily_carbs: Optional[int] = None

    daily_fat: Optional[int] = None

    daily_fiber: Optional[int] = None

    target_weight: Optional[float] = None

    allergies: Optional[str] = None

    health_conditions: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):

    name: Optional[str] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    height_cm: Optional[float] = None

    weight_kg: Optional[float] = None

    goal: Optional[str] = None

    activity_level: Optional[str] = None

    daily_budget: Optional[float] = None

    diet_preferences: Optional[str] = None

    target_weight: Optional[float] = None

    allergies: Optional[str] = None

    health_conditions: Optional[str] = None