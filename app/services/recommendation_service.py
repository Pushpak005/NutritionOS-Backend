from sqlalchemy import text

from app.database import engine

from app.services.recommendation_engine import (
    calculate_nutrition_score,
    get_recommendation_reasons
)

from app.services.meal_engine import (
    get_meal_target_calories
)

from app.core.policies.nutrition_policy import (
    can_recommend_full_meal
)

from app.core.state.nutrition_state import (
    build_nutrition_state
)


# ==========================================
# Build Ranked Recommendation List
# ==========================================

def _get_scored_recommendations(user: dict):

    user = dict(user)

    # ==========================================
    # Dashboard AI Pick
    # Currently based on Lunch
    # ==========================================
    meal_window = (
        user.get("meal_window")
        or "Lunch"
    )

    user["meal_target_calories"] = get_meal_target_calories(
        user["daily_calories"],
        meal_window
    )

    # ==========================================
    # Nutrition Completion Policy
    # ==========================================

    nutrition_state = build_nutrition_state(
        user["core_context"]
    )

    # Make centralized nutrition state available
    # to the recommendation layer.
    user["nutrition_state"] = nutrition_state

    if not can_recommend_full_meal(
        nutrition_state
    ):
        return []

    # ==========================================
    # Load Available Dishes
    # ==========================================

    with engine.connect() as conn:

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
                    m.image_key,
                    m.healthy_score,

                    r.restaurant_name,
                    r.area,
                    r.rating,
                    r.delivery_time

                FROM menu_items m

                JOIN restaurants r

                    ON r.restaurant_id = m.restaurant_id

                WHERE

                    m.available = TRUE

            """)

        ).mappings().all()

    recommendations = []

    # ==========================================
    # Score Every Dish
    # ==========================================

    for dish in dishes:

        # ==========================================
        # Veg Filter
        # ==========================================

        if (

            user.get("diet_preferences")

            and

            user["diet_preferences"].lower() == "veg"

            and

            not dish["is_veg"]

        ):

            continue

        # ==========================================
        # AI Nutrition Score
        # ==========================================

        score = calculate_nutrition_score(
            user,
            dish
        )

        # ==========================================
        # Dynamic AI Explanation
        # ==========================================

        why_recommended = get_recommendation_reasons(
            user,
            dish
        )

        # ==========================================
        # Build Recommendation
        # ==========================================

        recommendation = dict(dish)

        recommendation["score"] = score

        recommendation["match_percentage"] = score

        recommendation["why_recommended"] = (
            why_recommended
        )

        recommendations.append(
            recommendation
        )

    # ==========================================
    # Highest Score First
    # ==========================================

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


# ==========================================
# Today's Best AI Pick
# ==========================================

def get_best_recommendation(user: dict):

    recommendations = _get_scored_recommendations(
        user
    )

    if not recommendations:
        return None

    return recommendations[0]


# ==========================================
# Top AI Picks
# ==========================================

def get_top_recommendations(
    user: dict,
    limit: int = 5
):

    recommendations = _get_scored_recommendations(
        user
    )

    return recommendations[:limit]