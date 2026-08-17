from sqlalchemy import text

from app.database import engine


def get_weekly_analytics(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(

            text("""
                SELECT

                    DATE(ml.eaten_at) AS day,

                    SUM(
                        ml.calories
                    ) AS calories,

                    SUM(
                        ml.protein
                    ) AS protein,

                    SUM(
                        ml.carbs
                    ) AS carbs,

                    SUM(
                        ml.fat
                    ) AS fat

                FROM meal_logs ml

                WHERE

                    ml.user_id = :user_id

                    AND ml.eaten_at >= CURRENT_DATE - INTERVAL '6 days'

                    AND ml.eaten_at < CURRENT_DATE + INTERVAL '1 day'

                GROUP BY

                    DATE(ml.eaten_at)

                ORDER BY

                    DATE(ml.eaten_at) ASC

            """),

            {
                "user_id": user_id
            }

        ).fetchall()

    analytics = []

    for row in result:

        analytics.append({

            "day": str(row.day),

            "calories": float(
                row.calories or 0
            ),

            "protein": float(
                row.protein or 0
            ),

            "carbs": float(
                row.carbs or 0
            ),

            "fat": float(
                row.fat or 0
            )

        })

    return analytics