from sqlalchemy import text

from app.database import engine


def get_dashboard(user_id: int):

    with engine.connect() as conn:

        # ==========================================
        # User Profile
        # ==========================================

        profile = conn.execute(
            text("""
                SELECT
                    name,
                    goal,

                    bmi,

                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber

                FROM users

                WHERE id = :id
            """),
            {
                "id": user_id
            }
        ).fetchone()

        # ==========================================
        # Today's Consumed Nutrition
        # ==========================================

        totals = conn.execute(
            text("""
                SELECT

                    COALESCE(SUM(mi.calories * m.quantity), 0) AS calories,

                    COALESCE(SUM(mi.protein * m.quantity), 0) AS protein,

                    COALESCE(SUM(mi.carbs * m.quantity), 0) AS carbs,

                    COALESCE(SUM(mi.fat * m.quantity), 0) AS fat,

                    COALESCE(SUM(mi.fiber * m.quantity), 0) AS fiber

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id = mi.id

                WHERE m.user_id = :id
            """),
            {
                "id": user_id
            }
        ).fetchone()

    profile = dict(profile._mapping)
    totals = dict(totals._mapping)

    # ==========================================
    # Remaining Nutrition
    # ==========================================

    remaining = {

        "calories": max(
            profile["daily_calories"] - totals["calories"],
            0
        ),

        "protein": max(
            profile["daily_protein"] - totals["protein"],
            0
        ),

        "carbs": max(
            profile["daily_carbs"] - totals["carbs"],
            0
        ),

        "fat": max(
            profile["daily_fat"] - totals["fat"],
            0
        ),

        "fiber": max(
            profile["daily_fiber"] - totals["fiber"],
            0
        )

    }

    # ==========================================
    # Dashboard Response
    # ==========================================

    return {

        "profile": profile,

        "consumed": totals,

        "remaining": remaining

    }