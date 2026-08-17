from sqlalchemy import text

from app.database import engine


def calculate_score(user_id: int):

    with engine.connect() as conn:

        # ==========================================
        # User Nutrition Targets
        # ==========================================

        profile = conn.execute(

            text("""
                SELECT

                    daily_calories,

                    daily_protein

                FROM users

                WHERE id = :id
            """),

            {
                "id": user_id
            }

        ).mappings().first()

        if not profile:

            return {

                "score": 0,

                "calories": 0,

                "protein": 0

            }

        # ==========================================
        # Today's Nutrition
        # Source: meal_logs
        # ==========================================

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
                    ) AS protein

                FROM meal_logs

                WHERE

                    user_id = :id

                    AND DATE(eaten_at) = CURRENT_DATE

            """),

            {
                "id": user_id
            }

        ).mappings().first()

    # ==========================================
    # Safe Numeric Values
    # ==========================================

    daily_calories = float(
        profile["daily_calories"] or 0
    )

    daily_protein = float(
        profile["daily_protein"] or 0
    )

    consumed_calories = float(
        totals["calories"] or 0
    )

    consumed_protein = float(
        totals["protein"] or 0
    )

    # ==========================================
    # Nutrition Score
    # ==========================================

    score = 0

    # ------------------------------------------
    # Calories within daily target
    # ------------------------------------------

    if (

        daily_calories > 0

        and

        consumed_calories <= daily_calories

    ):

        score += 40

    # ------------------------------------------
    # Protein target progress
    # ------------------------------------------

    if (

        daily_protein > 0

        and

        consumed_protein >= daily_protein * 0.8

    ):

        score += 30

    # ------------------------------------------
    # At least 60% of calorie target consumed
    # ------------------------------------------

    if (

        daily_calories > 0

        and

        consumed_calories >= daily_calories * 0.6

    ):

        score += 20

    # ------------------------------------------
    # Any protein consumed
    # ------------------------------------------

    if consumed_protein > 0:

        score += 10

    # ==========================================
    # Response
    # ==========================================

    return {

        "score": score,

        "calories": consumed_calories,

        "protein": consumed_protein

    }