from sqlalchemy import text
from app.database import engine


def get_weekly_analytics(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(

            text("""

                SELECT

                    DATE(
                        COALESCE(
                            m.consumed_at,
                            m.created_at
                        )
                    ) AS day,

                    SUM(
                        mi.calories * CAST(m.quantity AS NUMERIC)
                    ) AS calories,

                    SUM(
                        CAST(mi.protein AS NUMERIC) * CAST(m.quantity AS NUMERIC)
                    ) AS protein,

                    SUM(
                        CAST(mi.carbs AS NUMERIC) * CAST(m.quantity AS NUMERIC)
                    ) AS carbs,

                    SUM(
                        CAST(mi.fat AS NUMERIC) * CAST(m.quantity AS NUMERIC)
                    ) AS fat

                FROM meals m

                JOIN menu_items mi

                    ON m.menu_item_id = mi.id

                WHERE m.user_id = :user_id

                GROUP BY

                    DATE(
                        COALESCE(
                            m.consumed_at,
                            m.created_at
                        )
                    )

                ORDER BY

                    DATE(
                        COALESCE(
                            m.consumed_at,
                            m.created_at
                        )
                    ) ASC

            """),

            {

                "user_id": user_id

            }

        ).fetchall()

    analytics = []

    for row in result:

        analytics.append({

            "day": str(row.day),

            "calories": float(row.calories or 0),

            "protein": float(row.protein or 0),

            "carbs": float(row.carbs or 0),

            "fat": float(row.fat or 0)

        })

    return analytics