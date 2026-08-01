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