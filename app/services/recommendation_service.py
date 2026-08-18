from sqlalchemy import text

from app.database import engine

from app.services.recommendation_engine import (
    calculate_nutrition_score,
    get_recommendation_reasons
)

from app.services.meal_engine import (
    get_meal_target_calories
)

from app.core.policies.action_policy import (
    evaluate_meal_action
)


# ==========================================
# Normalize Meal Window
# ==========================================

def _normalize_meal_window(
    meal_window: str
) -> str:

    if not meal_window:

        return "Lunch"

    normalized = str(
        meal_window
    ).strip().lower()

    meal_windows = {

        "breakfast":
            "Breakfast",

        "lunch":
            "Lunch",

        "dinner":
            "Dinner",

        "snack":
            "Snack",

        "late night":
            "Late Night"

    }

    return meal_windows.get(
        normalized,
        "Lunch"
    )


# ==========================================
# Build Ranked Recommendation List
# ==========================================

def _get_scored_recommendations(
    user: dict
):

    user = dict(user)

    # ==========================================
    # Centralized Action Policy
    #
    # The action policy owns the complete
    # deterministic decision of whether a
    # normal meal recommendation is allowed.
    #
    # It internally evaluates:
    #
    # - current meal policy
    # - nutrition completion policy
    #
    # Recommendation service therefore does
    # not directly orchestrate individual
    # business policies.
    # ==========================================

    core_context = user.get(
        "core_context"
    )

    if core_context is not None:

        action_decision = evaluate_meal_action(
            core_context
        )

        if not action_decision.allowed:

            return []

    # ==========================================
    # Dashboard Meal Window
    # ==========================================

    meal_window = _normalize_meal_window(
        user.get("meal_window")
    )

    user["meal_window"] = meal_window

    # ==========================================
    # Late Night Safety Guard
    #
    # There is currently no dedicated
    # Late Night menu category.
    #
    # Never silently convert Late Night
    # into another meal.
    # ==========================================

    if meal_window == "Late Night":

        return []

    # ==========================================
    # Meal-Specific Calorie Target
    # ==========================================

    user["meal_target_calories"] = (
        get_meal_target_calories(
            user["daily_calories"],
            meal_window
        )
    )

    # ==========================================
    # Centralized Nutrition State
    #
    # Nutrition state is already prepared by
    # the action policy and recommendation
    # context flow.
    #
    # Keep the existing state assignment so
    # downstream scoring and explanations can
    # continue consuming nutrition_state.
    # ==========================================

    nutrition_state = user.get(
        "nutrition_state"
    )

    if nutrition_state is not None:

        user["nutrition_state"] = (
            nutrition_state
        )

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

                    ON r.restaurant_id =
                       m.restaurant_id

                WHERE

                    m.available = TRUE

                    AND LOWER(
                        m.meal_type
                    ) = LOWER(
                        :meal_window
                    )

            """),

            {
                "meal_window":
                    meal_window
            }

        ).mappings().all()

    recommendations = []

    # ==========================================
    # Score Eligible Dishes
    # ==========================================

    for dish in dishes:

        # ==========================================
        # Veg Filter
        # ==========================================

        if (

            user.get(
                "diet_preferences"
            )

            and

            user[
                "diet_preferences"
            ].lower() == "veg"

            and

            not dish[
                "is_veg"
            ]

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

        why_recommended = (
            get_recommendation_reasons(
                user,
                dish
            )
        )

        # ==========================================
        # Build Recommendation
        # ==========================================

        recommendation = dict(
            dish
        )

        recommendation[
            "score"
        ] = score

        recommendation[
            "match_percentage"
        ] = score

        recommendation[
            "why_recommended"
        ] = why_recommended

        recommendations.append(
            recommendation
        )

    # ==========================================
    # Highest Score First
    # ==========================================

    recommendations.sort(

        key=lambda x:
            x["score"],

        reverse=True

    )

    return recommendations


# ==========================================
# Today's Best AI Pick
# ==========================================

def get_best_recommendation(
    user: dict
):

    recommendations = (
        _get_scored_recommendations(
            user
        )
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

    recommendations = (
        _get_scored_recommendations(
            user
        )
    )

    return recommendations[
        :limit
    ]