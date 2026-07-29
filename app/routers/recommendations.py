from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text

from app.database import engine
from app.utils.auth_dependency import get_current_user
from app.services.recommendation_engine import calculate_nutrition_score
from app.services.meal_engine import get_meal_target_calories

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/")
def get_recommendations(
    meal: str = Query(
        ...,
        description="Breakfast | Lunch | Dinner | Snack"
    ),
    current_user=Depends(get_current_user)
):

    meal = meal.capitalize()

    if meal not in ["Breakfast", "Lunch", "Dinner", "Snack"]:
        raise HTTPException(
            status_code=400,
            detail="Meal must be Breakfast, Lunch, Dinner or Snack."
        )

    with engine.connect() as conn:

        # -----------------------
        # Logged In User
        # -----------------------

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

        # -----------------------
        # Meal Target Calories
        # -----------------------

        meal_target = get_meal_target_calories(
            user["daily_calories"],
            meal
        )

        user = dict(user)
        user["meal_target_calories"] = meal_target

        # -----------------------
        # Menu + Restaurant
        # -----------------------

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
                    m.image_url,

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

    for dish in dishes:

        # -----------------------
        # Veg Filter
        # -----------------------

        if (
            user.get("diet_preferences")
            and user["diet_preferences"].lower() == "veg"
            and not dish["is_veg"]
        ):
            continue

        # -----------------------
        # Nutrition Score
        # -----------------------

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

            "rating": float(dish["rating"] or 0),

            "delivery_time": dish["delivery_time"],

            "category": dish["category"],

            "calories": dish["calories"],

            "protein": float(dish["protein"] or 0),

            "carbs": float(dish["carbs"] or 0),

            "fat": float(dish["fat"] or 0),

            "fiber": float(dish["fiber"] or 0),

            "price": float(dish["price"] or 0),

            "is_veg": dish["is_veg"],

            "image_url": dish["image_url"],

            "score": score

        })
    
    # -----------------------
    # Highest Score First
    # -----------------------

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {

        "success": True,

        "meal": meal,

        "target_calories": round(meal_target),

        "total_recommendations": len(recommendations),

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
                    m.image_url,

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

    # ----------------------------------
    # Recommendation Explanation
    # ----------------------------------

    why_recommended = []

    if dish["protein"] and dish["protein"] >= 25:
        why_recommended.append("Excellent source of protein.")

    if dish["calories"] and dish["calories"] <= 700:
        why_recommended.append("Fits your meal calorie target.")

    if dish["price"] and dish["price"] <= 250:
        why_recommended.append("Budget friendly meal.")

    if dish["is_veg"]:
        why_recommended.append("Suitable for vegetarian diet.")

    if dish["rating"] and float(dish["rating"]) >= 4.5:
        why_recommended.append("Highly rated restaurant.")

    return {

        "success": True,

        "dish": {

            "dish_id": dish["id"],

            "dish_name": dish["dish_name"],

            "meal_type": dish["meal_type"],

            "category": dish["category"],

            "restaurant": dish["restaurant_name"],

            "area": dish["area"],

            "rating": float(dish["rating"] or 0),

            "delivery_time": dish["delivery_time"],

            "calories": dish["calories"],

            "protein": float(dish["protein"] or 0),

            "carbs": float(dish["carbs"] or 0),

            "fat": float(dish["fat"] or 0),

            "fiber": float(dish["fiber"] or 0),

            "price": float(dish["price"] or 0),

            "is_veg": dish["is_veg"],

            "image_url": dish["image_url"]

        },

        "why_recommended": why_recommended

    }