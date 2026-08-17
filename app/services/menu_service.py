from sqlalchemy import text
from app.database import engine


def get_menu_by_restaurant(restaurant_id: int):

    with engine.connect() as conn:

        result = conn.execute(

            text("""

                SELECT

                    id,

                    restaurant_id,

                    dish_name,

                    category,

                    meal_type,

                    calories,

                    protein,

                    carbs,

                    fat,

                    fiber,

                    price,

                    is_veg,

                    healthy_score,

                    image_key,

                    description,

                    cuisine,

                    ingredients,

                    spice_level,

                    prep_time,

                    popularity_score

                FROM menu_items

                WHERE restaurant_id = :restaurant_id

                  AND available = TRUE

                ORDER BY price

            """),

            {

                "restaurant_id": restaurant_id

            }

        ).mappings().all()

    return [dict(row) for row in result]