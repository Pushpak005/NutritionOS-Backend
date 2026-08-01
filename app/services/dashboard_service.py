from sqlalchemy import text
from app.database import engine


def get_dashboard(user_id: int):

    with engine.connect() as conn:

        profile = conn.execute(
            text("""
                SELECT
                    name,
                    goal,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat
                FROM users
                WHERE id=:id
            """),
            {
                "id": user_id
            }
        ).fetchone()

        totals = conn.execute(
            text("""
                SELECT

                    COALESCE(SUM(mi.calories * m.quantity),0) calories,

                    COALESCE(SUM(mi.protein * m.quantity),0) protein,

                    COALESCE(SUM(mi.carbs * m.quantity),0) carbs,

                    COALESCE(SUM(mi.fat * m.quantity),0) fat

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id = mi.id

                WHERE m.user_id=:id
            """),
            {
                "id": user_id
            }
        ).fetchone()

    profile = dict(profile._mapping)
    totals = dict(totals._mapping)

    return {
        "profile": profile,
        "consumed": totals
    }