from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text

from app.database import engine
from app.utils.auth_dependency import get_current_user

from app.core.context.context_factory import ContextFactory
from app.core.policies.action_policy import evaluate_meal_action


from app.services.recommendation_engine import (
    calculate_nutrition_score
)

from app.services.meal_engine import (
    get_meal_target_calories
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# ==========================================================
# Recommendation List
# ==========================================================

@router.get("/")
def get_recommendations(
    meal: str = Query(
        ...,
        description="Breakfast | Lunch | Dinner | Snack"
    ),
    current_user=Depends(get_current_user)
):

    meal = meal.capitalize()

    core_context = ContextFactory().build(
        current_user["user_id"]
    )

    action_decision = evaluate_meal_action(
        core_context
    )

    if not action_decision.allowed:

        return {
            "success": True,
            "meal": meal,
            "blocked": True,
            "reason": action_decision.reason,
            "total_recommendations": 0,
            "recommendations": []
        }


    if meal not in [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Meal must be Breakfast, Lunch, Dinner or Snack."
        )

    with engine.connect() as conn:

        # ==================================================
        # Logged In User
        # ==================================================

        user = conn.execute(

            text("""
                SELECT *

                FROM users

                WHERE id = :id
            """),

            {
                "id": current_user["user_id"]
            }

        ).mappings().first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        user = dict(user)

        # ==================================================
        # Today's Nutrition
        # ==================================================

        totals = conn.execute(

            text("""
                SELECT

                    COALESCE(
                        SUM(calories),
                        0
                    ) AS calories,

                    COALESCE(
                        SUM(protein),
                        0
                    ) AS protein,

                    COALESCE(
                        SUM(carbs),
                        0
                    ) AS carbs,

                    COALESCE(
                        SUM(fat),
                        0
                    ) AS fat,

                    COALESCE(
                        SUM(fiber),
                        0
                    ) AS fiber,

                    COUNT(*) AS meals_logged

                FROM meal_logs

                WHERE

                    user_id = :user_id

                    AND DATE(eaten_at) = CURRENT_DATE
            """),

            {
                "user_id": current_user["user_id"]
            }

        ).mappings().first()

        totals = dict(totals)

        # ==================================================
        # Remaining Nutrition
        # ==================================================

        remaining = {

            "calories": max(

                (user["daily_calories"] or 0)
                - float(totals["calories"] or 0),

                0

            ),

            "protein": max(

                (user["daily_protein"] or 0)
                - float(totals["protein"] or 0),

                0

            ),

            "carbs": max(

                (user["daily_carbs"] or 0)
                - float(totals["carbs"] or 0),

                0

            ),

            "fat": max(

                (user["daily_fat"] or 0)
                - float(totals["fat"] or 0),

                0

            ),

            "fiber": max(

                (user["daily_fiber"] or 0)
                - float(totals["fiber"] or 0),

                0

            )

        }

        # ==================================================
        # Recommendation Context
        # ==================================================

        user["consumed"] = totals

        user["remaining"] = remaining

        # ==================================================
        # Meal Target Calories
        # ==================================================

        meal_target = get_meal_target_calories(

            user["daily_calories"],

            meal

        )

        user["meal_target_calories"] = meal_target

        # ==================================================
        # Menu + Restaurant
        # ==================================================

        dishes = conn.execute(

            text("""
                SELECT

                    m.id,
                    m.restaurant_id,
                    m.dish_name,
                    m.category,
                    m.meal_type,
                    m.calories,
                    m.protein,
                    m.carbs,
                    m.fat,
                    m.fiber,
                    m.price,
                    m.is_veg,
                    m.available,
                    m.image_key,
                    m.healthy_score,

                    r.restaurant_name,
                    r.area,
                    r.rating,
                    r.delivery_time

                FROM menu_items m

                JOIN restaurants r
                    ON m.restaurant_id = r.restaurant_id

                WHERE

                    m.available = TRUE

                    AND m.meal_type = :meal
            """),

            {
                "meal": meal
            }

        ).mappings().all()

    recommendations = []

    # ======================================================
    # Score Every Dish
    # ======================================================

    for dish in dishes:

        # --------------------------------------------------
        # Veg Filter
        # --------------------------------------------------

        if (

            user.get("diet_preferences")

            and

            user["diet_preferences"].lower() == "veg"

            and

            not dish["is_veg"]

        ):

            continue

        # --------------------------------------------------
        # Nutrition Score
        # --------------------------------------------------

        score = calculate_nutrition_score(

            user,

            dish

        )

        recommendations.append({

            "dish_id": dish["id"],

            "dish_name": dish["dish_name"],

            "meal_type": dish["meal_type"],

            "restaurant": dish["restaurant_name"],

            "area": dish["area"],

            "rating": float(
                dish["rating"] or 0
            ),

            "delivery_time": dish["delivery_time"],

            "category": dish["category"],

            "calories": dish["calories"],

            "protein": float(
                dish["protein"] or 0
            ),

            "carbs": float(
                dish["carbs"] or 0
            ),

            "fat": float(
                dish["fat"] or 0
            ),

            "fiber": float(
                dish["fiber"] or 0
            ),

            "price": float(
                dish["price"] or 0
            ),

            "is_veg": dish["is_veg"],

            "healthy_score": dish["healthy_score"],

            "image_key": dish["image_key"],

            "score": score

        })

    # ======================================================
    # Highest Score First
    # ======================================================

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return {

        "success": True,

        "meal": meal,

        "target_calories": round(
            meal_target
        ),

        "consumed": totals,

        "remaining": remaining,

        "total_recommendations": len(
            recommendations
        ),

        "recommendations": recommendations[:10]

    }


# ==========================================================
# Recommendation Details
# ==========================================================

@router.get("/{dish_id}")
def get_recommendation_details(
    dish_id: int,
    current_user=Depends(get_current_user)
):

    with engine.connect() as conn:

        # ==================================================
        # Dish
        # ==================================================

        dish = conn.execute(

            text("""
                SELECT

                    m.id,
                    m.restaurant_id,
                    m.dish_name,
                    m.category,
                    m.meal_type,
                    m.calories,
                    m.protein,
                    m.carbs,
                    m.fat,
                    m.fiber,
                    m.price,
                    m.is_veg,
                    m.available,
                    m.image_key,
                    m.healthy_score,

                    r.restaurant_name,
                    r.area,
                    r.rating,
                    r.delivery_time

                FROM menu_items m

                JOIN restaurants r
                    ON m.restaurant_id = r.restaurant_id

                WHERE

                    m.id = :dish_id
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

        # ==================================================
        # User Profile
        # ==================================================

        user = conn.execute(

            text("""
                SELECT

                    id,
                    goal,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber,
                    daily_budget,
                    diet_preferences

                FROM users

                WHERE id = :user_id
            """),

            {
                "user_id": current_user["user_id"]
            }

        ).mappings().first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # ==================================================
        # Today's Nutrition
        # ==================================================

        totals = conn.execute(

            text("""
                SELECT

                    COALESCE(
                        SUM(calories),
                        0
                    ) AS calories,

                    COALESCE(
                        SUM(protein),
                        0
                    ) AS protein,

                    COALESCE(
                        SUM(carbs),
                        0
                    ) AS carbs,

                    COALESCE(
                        SUM(fat),
                        0
                    ) AS fat,

                    COALESCE(
                        SUM(fiber),
                        0
                    ) AS fiber

                FROM meal_logs

                WHERE

                    user_id = :user_id

                    AND DATE(eaten_at) = CURRENT_DATE
            """),

            {
                "user_id": current_user["user_id"]
            }

        ).mappings().first()

        totals = dict(totals)

        # ==================================================
        # Remaining Nutrition
        # ==================================================

        remaining = {

            "calories": max(

                (user["daily_calories"] or 0)
                - float(totals["calories"] or 0),

                0

            ),

            "protein": max(

                (user["daily_protein"] or 0)
                - float(totals["protein"] or 0),

                0

            ),

            "carbs": max(

                (user["daily_carbs"] or 0)
                - float(totals["carbs"] or 0),

                0

            ),

            "fat": max(

                (user["daily_fat"] or 0)
                - float(totals["fat"] or 0),

                0

            ),

            "fiber": max(

                (user["daily_fiber"] or 0)
                - float(totals["fiber"] or 0),

                0

            )

        }

        # ==================================================
        # Dynamic Recommendation Reasons
        # ==================================================

        why_recommended = []

        if (

            dish["protein"]

            and

            float(dish["protein"]) >= 25

        ):

            why_recommended.append(
                "Excellent source of protein."
            )

        if (

            remaining["protein"] > 0

            and

            dish["protein"]

            and

            float(dish["protein"])
            <= remaining["protein"]

        ):

            why_recommended.append(
                "Helps cover your remaining protein target."
            )

        if (

            remaining["calories"] > 0

            and

            dish["calories"]

            and

            float(dish["calories"])
            <= remaining["calories"]

        ):

            why_recommended.append(
                "Fits within your remaining calorie budget."
            )

        if (

            dish["price"]

            and

            user["daily_budget"]

            and

            float(dish["price"])
            <= float(user["daily_budget"])

        ):

            why_recommended.append(
                "Fits within your daily food budget."
            )

        if dish["is_veg"]:

            why_recommended.append(
                "Suitable for vegetarian diet."
            )

        if (

            dish["rating"]

            and

            float(dish["rating"]) >= 4.5

        ):

            why_recommended.append(
                "Highly rated restaurant."
            )

        if not why_recommended:

            why_recommended.append(
                "Selected based on your current nutrition profile."
            )

    return {

        "success": True,

        "dish": {

            "dish_id": dish["id"],

            "dish_name": dish["dish_name"],

            "meal_type": dish["meal_type"],

            "category": dish["category"],

            "restaurant": dish["restaurant_name"],

            "area": dish["area"],

            "rating": float(
                dish["rating"] or 0
            ),

            "delivery_time": dish["delivery_time"],

            "calories": dish["calories"],

            "protein": float(
                dish["protein"] or 0
            ),

            "carbs": float(
                dish["carbs"] or 0
            ),

            "fat": float(
                dish["fat"] or 0
            ),

            "fiber": float(
                dish["fiber"] or 0
            ),

            "price": float(
                dish["price"] or 0
            ),

            "is_veg": dish["is_veg"],

            "healthy_score": dish["healthy_score"],

            "image_key": dish["image_key"]

        },

        "why_recommended": why_recommended

    }
