from sqlalchemy import text
from app.database import engine


def get_menu_by_restaurant(restaurant_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    dish_name,
                    category,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber,
                    price,
                    is_veg,
                    meal_type
                FROM menu_items
                WHERE restaurant_id = :restaurant_id
                  AND available = TRUE
                ORDER BY price
            """),
            {
                "restaurant_id": restaurant_id
            }
        ).fetchall()

    return [dict(row._mapping) for row in result]