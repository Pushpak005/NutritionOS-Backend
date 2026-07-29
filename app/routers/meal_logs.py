from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from app.database import engine
from app.utils.auth_dependency import get_current_user

router = APIRouter(
    prefix="/meal-log",
    tags=["Meal Log"]
)


# ==========================================================
# Log Meal
# ==========================================================

@router.post("/{dish_id}")
def log_meal(
    dish_id: int,
    current_user=Depends(get_current_user)
):

    with engine.begin() as conn:

        # ------------------------
        # Check Dish Exists
        # ------------------------

        dish = conn.execute(
            text("""
                SELECT *
                FROM menu_items
                WHERE id = :dish_id
            """),
            {
                "dish_id": dish_id
            }
        ).mappings().first()

        if not dish:
            raise HTTPException(
                status_code=404,
                detail="Dish not found."
            )

        # ------------------------
        # Insert Meal Log
        # ------------------------

        conn.execute(
            text("""
                INSERT INTO meal_logs
                (
                    user_id,
                    dish_id,
                    meal_type,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber
                )

                VALUES
                (
                    :user_id,
                    :dish_id,
                    :meal_type,
                    :calories,
                    :protein,
                    :carbs,
                    :fat,
                    :fiber
                )
            """),
            {

                "user_id": current_user["user_id"],

                "dish_id": dish["id"],

                "meal_type": dish["meal_type"],

                "calories": dish["calories"],

                "protein": dish["protein"],

                "carbs": dish["carbs"],

                "fat": dish["fat"],

                "fiber": dish["fiber"]

            }
        )

    return {

        "success": True,

        "message": "Meal logged successfully.",

        "dish": dish["dish_name"],

        "meal_type": dish["meal_type"],

        "calories": dish["calories"]

    }


# ==========================================================
# Today's Meal Logs
# ==========================================================

@router.get("/today")
def get_today_meals(
    current_user=Depends(get_current_user)
):

    with engine.connect() as conn:

        # ------------------------
        # Get Today's Meals
        # ------------------------

        logs = conn.execute(
            text("""
                SELECT
                    id,
                    dish_id,
                    meal_type,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber,
                    eaten_at

                FROM meal_logs

                WHERE
                    user_id = :user_id
                    AND DATE(eaten_at) = CURRENT_DATE

                ORDER BY eaten_at
            """),
            {
                "user_id": current_user["user_id"]
            }
        ).mappings().all()

        # ------------------------
        # User Daily Target
        # ------------------------

        user = conn.execute(
            text("""
                SELECT
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber

                FROM users

                WHERE id = :id
            """),
            {
                "id": current_user["user_id"]
            }
        ).mappings().first()

    # ------------------------
    # Totals
    # ------------------------

    total_calories = sum(log["calories"] or 0 for log in logs)

    total_protein = sum(float(log["protein"] or 0) for log in logs)

    total_carbs = sum(float(log["carbs"] or 0) for log in logs)

    total_fat = sum(float(log["fat"] or 0) for log in logs)

    total_fiber = sum(float(log["fiber"] or 0) for log in logs)

    remaining_calories = max(
        0,
        user["daily_calories"] - total_calories
    )

    return {

        "success": True,

        "daily_target": user["daily_calories"],

        "consumed_calories": total_calories,

        "remaining_calories": remaining_calories,

        "target_protein": float(user["daily_protein"] or 0),

        "consumed_protein": total_protein,

        "target_carbs": float(user["daily_carbs"] or 0),

        "consumed_carbs": total_carbs,

        "target_fat": float(user["daily_fat"] or 0),

        "consumed_fat": total_fat,

        "target_fiber": float(user["daily_fiber"] or 0),

        "consumed_fiber": total_fiber,

        "total_meals": len(logs),

        "meals": logs

    }