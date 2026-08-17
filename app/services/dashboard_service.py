from sqlalchemy import text

from app.database import engine

from app.core.core_service import CoreService

from app.services.recommendation_service import (
    get_best_recommendation,
    get_top_recommendations
)


# ==========================================
# Core Service
# ==========================================

core_service = CoreService()


# ==========================================
# Dashboard
# ==========================================

def get_dashboard(user_id: int):

    # ==========================================
    # Core Nutrition Context
    #
    # CoreService is now the authoritative
    # source for the user's current nutrition
    # state.
    # ==========================================

    context = core_service.get_context(
        user_id
    )

    with engine.connect() as conn:

        # ==========================================
        # User Profile
        # ==========================================

        profile = conn.execute(

            text("""
                SELECT

                    id,
                    name,
                    goal,
                    bmi,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber,
                    daily_budget,
                    diet_preferences

                FROM users

                WHERE id = :id
            """),

            {
                "id": user_id
            }

        ).mappings().first()

        if not profile:

            return {
                "message": "User not found."
            }

        profile = dict(profile)

        # ==========================================
        # Today's Nutrition
        #
        # Source: meal_logs
        #
        # This remains in the dashboard response
        # because the frontend needs the consumed
        # values.
        #
        # Remaining nutrition is NOT calculated here.
        # CoreService already owns that calculation.
        # ==========================================

        totals = conn.execute(

            text("""
                SELECT

                    COALESCE(
                        SUM(calories),
                        0
                    ) calories,

                    COALESCE(
                        SUM(protein),
                        0
                    ) protein,

                    COALESCE(
                        SUM(carbs),
                        0
                    ) carbs,

                    COALESCE(
                        SUM(fat),
                        0
                    ) fat,

                    COALESCE(
                        SUM(fiber),
                        0
                    ) fiber,

                    COUNT(*) meals_logged

                FROM meal_logs

                WHERE

                    user_id = :id

                    AND DATE(eaten_at) = CURRENT_DATE

            """),

            {
                "id": user_id
            }

        ).mappings().first()

        totals = dict(totals)

        # ==========================================
        # Remaining Nutrition
        #
        # IMPORTANT:
        #
        # Do NOT recalculate remaining nutrition
        # from profile + totals here.
        #
        # CoreService / ContextFactory is now the
        # single source of truth.
        # ==========================================

        remaining = {

            "calories":
                float(
                    context.remaining_calories or 0
                ),

            "protein":
                float(
                    context.remaining_protein or 0
                ),

            "carbs":
                float(
                    context.remaining_carbs or 0
                ),

            "fat":
                float(
                    context.remaining_fat or 0
                ),

            "fiber":
                float(
                    context.remaining_fiber or 0
                )

        }

        # ==========================================
        # Nutrition Completion State
        # ==========================================

        nutrition_complete = (

            remaining["calories"] <= 100

            and

            remaining["protein"] <= 0

        )

        # ==========================================
        # Recommendation Context
        #
        # Existing recommendation engine still
        # receives the same profile + consumed +
        # remaining structure.
        #
        # Core meal_window is now also available
        # to the recommendation layer.
        # ==========================================

        recommendation_context = {

            **profile,

            "consumed": totals,

            "remaining": remaining,

            "meal_window":
                context.meal_window,

            "core_context":
                context

        }

        # ==========================================
        # AI Recommendations
        # ==========================================

        today_ai_pick = get_best_recommendation(
            recommendation_context
        )

        top_ai_picks = get_top_recommendations(
            recommendation_context,
            limit=5
        )

        # ==========================================
        # Dashboard Response
        # ==========================================

        return {

            "profile":
                profile,

            "consumed":
                totals,

            "remaining":
                remaining,

            "nutrition_complete":
                nutrition_complete,

            "today_ai_pick":
                today_ai_pick,

            "top_ai_picks":
                top_ai_picks

        }