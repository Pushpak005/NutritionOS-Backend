from sqlalchemy import text
from app.database import engine


def get_my_meals(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT

                    m.id,

                    mi.dish_name,

                    m.meal_type,

                    m.quantity,

                    mi.calories,

                    mi.protein,

                    mi.carbs,

                    mi.fat,

                    mi.fiber,

                    m.created_at

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id = mi.id

                WHERE m.user_id = :user_id

                ORDER BY m.created_at DESC

            """),
            {
                "user_id": user_id
            }
        ).fetchall()

    return [dict(row._mapping) for row in result]