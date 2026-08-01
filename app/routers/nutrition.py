from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import engine
from app.utils.auth_dependency import get_current_user
from app.services.nutrition_service import calculate_nutrition

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutrition"]
)


@router.post("/calculate")
def calculate(current_user=Depends(get_current_user)):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                SELECT
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    activity_level,
                    goal
                FROM users
                WHERE id = :id
            """),
            {
                "id": current_user["user_id"]
            }
        ).fetchone()

        if result is None:
            return {
                "success": False,
                "message": "User not found."
            }

        user = dict(result._mapping)

        nutrition = calculate_nutrition(
            gender=user["gender"],
            age=user["age"],
            height_cm=float(user["height_cm"]),
            weight_kg=float(user["weight_kg"]),
            activity_level=user["activity_level"],
            goal=user["goal"]
        )

        conn.execute(
            text("""
                UPDATE users
                SET
                    bmi = :bmi,
                    daily_calories = :daily_calories,
                    daily_protein = :daily_protein,
                    daily_carbs = :daily_carbs,
                    daily_fat = :daily_fat,
                    daily_fiber = :daily_fiber
                WHERE id = :id
            """),
            {
                "id": current_user["user_id"],
                **nutrition
            }
        )

    return {
        "success": True,
        "nutrition": nutrition
    }