from sqlalchemy import text

from app.database import engine


def calculate_score(user_id: int):

    with engine.connect() as conn:

        profile = conn.execute(

            text("""

                SELECT

                    daily_calories,

                    daily_protein

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

                    COALESCE(SUM(mi.calories * CAST(m.quantity AS NUMERIC)),0) calories,

                    COALESCE(SUM(CAST(mi.protein AS NUMERIC) * CAST(m.quantity AS NUMERIC)),0) protein

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id = mi.id

                WHERE m.user_id=:id

            """),

            {

                "id": user_id

            }

        ).fetchone()

    score = 0

    if totals.calories <= profile.daily_calories:

        score += 40

    if totals.protein >= profile.daily_protein * 0.8:

        score += 30

    if totals.calories >= profile.daily_calories * 0.6:

        score += 20

    if totals.protein > 0:

        score += 10

    return {

        "score": score,

        "calories": float(totals.calories),

        "protein": float(totals.protein)

    }
