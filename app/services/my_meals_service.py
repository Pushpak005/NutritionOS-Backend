from sqlalchemy import text

from app.database import engine


def get_my_meals(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(

            text("""
                SELECT

                    ml.id,

                    ml.dish_id,

                    mi.dish_name,

                    ml.meal_type,

                    ml.quantity,

                    ml.calories,

                    ml.protein,

                    ml.carbs,

                    ml.fat,

                    ml.fiber,

                    ml.source,

                    ml.status,

                    ml.eaten_at

                FROM meal_logs ml

                JOIN menu_items mi

                    ON ml.dish_id = mi.id

                WHERE

                    ml.user_id = :user_id

                    AND DATE(ml.eaten_at) = CURRENT_DATE

                ORDER BY

                    ml.eaten_at DESC

            """),

            {
                "user_id": user_id
            }

        ).fetchall()

    return [
        dict(row._mapping)
        for row in result
    ]