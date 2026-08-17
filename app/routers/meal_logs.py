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

        # --------------------------------------------------
        # Check Dish Exists
        # --------------------------------------------------

        dish = conn.execute(

            text("""
                SELECT

                    id,
                    dish_name,
                    meal_type,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber

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


        # --------------------------------------------------
        # Insert Meal Log
        # --------------------------------------------------

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

                "user_id":
                    current_user["user_id"],

                "dish_id":
                    dish["id"],

                "meal_type":
                    dish["meal_type"],

                "calories":
                    dish["calories"],

                "protein":
                    dish["protein"],

                "carbs":
                    dish["carbs"],

                "fat":
                    dish["fat"],

                "fiber":
                    dish["fiber"]

            }

        )


    return {

        "success": True,

        "message":
            "Meal logged successfully.",

        "dish":
            dish["dish_name"],

        "meal_type":
            dish["meal_type"],

        "calories":
            dish["calories"]

    }


# ==========================================================
# Today's Meal Logs
# ==========================================================

@router.get("/today")
def get_today_meals(
    current_user=Depends(get_current_user)
):

    with engine.connect() as conn:

        # ==================================================
        # Today's Meals
        #
        # JOIN menu_items so frontend receives:
        #
        # dish_name
        # image_key
        # healthy_score
        # price
        # restaurant
        #
        # Nutrition Event metadata:
        #
        # source
        # status
        # ==================================================

        logs = conn.execute(

            text("""
                SELECT

                    ml.id,

                    ml.dish_id,

                    ml.meal_type,

                    ml.calories,

                    ml.protein,

                    ml.carbs,

                    ml.fat,

                    ml.fiber,

                    ml.quantity,

                    ml.source,

                    ml.status,

                    ml.eaten_at,


                    -- Dish Information

                    m.dish_name,

                    m.image_key,

                    m.healthy_score,

                    m.price,

                    m.category,

                    m.is_veg,


                    -- Restaurant Information

                    r.restaurant_name,

                    r.area,

                    r.rating,

                    r.delivery_time


                FROM meal_logs ml


                JOIN menu_items m

                    ON m.id = ml.dish_id


                LEFT JOIN restaurants r

                    ON r.restaurant_id =
                       m.restaurant_id


                WHERE

                    ml.user_id = :user_id

                    AND DATE(ml.eaten_at)
                        = CURRENT_DATE


                ORDER BY

                    ml.eaten_at DESC

            """),

            {
                "user_id":
                    current_user["user_id"]
            }

        ).mappings().all()


        # ==================================================
        # User Daily Targets
        # ==================================================

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
                "id":
                    current_user["user_id"]
            }

        ).mappings().first()


    # ======================================================
    # User Not Found
    # ======================================================

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    # ======================================================
    # Convert Rows
    # ======================================================

    meals = [
        dict(log)
        for log in logs
    ]


    # ======================================================
    # Today's Totals
    # ======================================================

    total_calories = sum(

        float(
            meal["calories"] or 0
        )

        for meal in meals

    )


    total_protein = sum(

        float(
            meal["protein"] or 0
        )

        for meal in meals

    )


    total_carbs = sum(

        float(
            meal["carbs"] or 0
        )

        for meal in meals

    )


    total_fat = sum(

        float(
            meal["fat"] or 0
        )

        for meal in meals

    )


    total_fiber = sum(

        float(
            meal["fiber"] or 0
        )

        for meal in meals

    )


    # ======================================================
    # Remaining Calories
    # ======================================================

    remaining_calories = max(

        0,

        float(
            user["daily_calories"] or 0
        )
        - total_calories

    )


    # ======================================================
    # Response
    # ======================================================

    return {

        "success": True,


        # --------------------------------------------------
        # Daily Targets
        # --------------------------------------------------

        "daily_target":
            float(
                user["daily_calories"] or 0
            ),

        "target_protein":
            float(
                user["daily_protein"] or 0
            ),

        "target_carbs":
            float(
                user["daily_carbs"] or 0
            ),

        "target_fat":
            float(
                user["daily_fat"] or 0
            ),

        "target_fiber":
            float(
                user["daily_fiber"] or 0
            ),


        # --------------------------------------------------
        # Consumed
        # --------------------------------------------------

        "consumed_calories":
            total_calories,

        "consumed_protein":
            total_protein,

        "consumed_carbs":
            total_carbs,

        "consumed_fat":
            total_fat,

        "consumed_fiber":
            total_fiber,


        # --------------------------------------------------
        # Remaining
        # --------------------------------------------------

        "remaining_calories":
            remaining_calories,


        # --------------------------------------------------
        # Meal Count
        # --------------------------------------------------

        "total_meals":
            len(meals),


        # --------------------------------------------------
        # Individual Meals
        # --------------------------------------------------

        "meals":
            meals

    }