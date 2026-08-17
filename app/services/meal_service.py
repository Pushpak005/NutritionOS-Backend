from sqlalchemy import text

from app.database import engine


def log_meal(
    user_id,
    menu_item_id,
    meal_type,
    quantity
):

    with engine.begin() as conn:

        # ==========================================
        # Get Dish Nutrition
        # ==========================================

        dish = conn.execute(

            text("""
                SELECT

                    id,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber

                FROM menu_items

                WHERE id = :menu_item_id

            """),

            {
                "menu_item_id": menu_item_id
            }

        ).mappings().first()

        if not dish:

            return {
                "success": False,
                "message": "Dish not found."
            }

        # ==========================================
        # Create Nutrition Event
        # ==========================================

        conn.execute(

            text("""
                INSERT INTO meal_logs
                (
                    user_id,
                    dish_id,
                    meal_type,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber,
                    eaten_at,
                    quantity,
                    source,
                    status
                )

                VALUES
                (
                    :user_id,
                    :dish_id,
                    :meal_type,
                    :calories,
                    :protein,
                    :carbs,
                    :fat,
                    :fiber,
                    CURRENT_TIMESTAMP,
                    :quantity,
                    :source,
                    :status
                )
            """),

            {
                "user_id": user_id,

                "dish_id": menu_item_id,

                "meal_type": meal_type,

                "calories":
                    float(dish["calories"] or 0)
                    * float(quantity),

                "protein":
                    float(dish["protein"] or 0)
                    * float(quantity),

                "carbs":
                    float(dish["carbs"] or 0)
                    * float(quantity),

                "fat":
                    float(dish["fat"] or 0)
                    * float(quantity),

                "fiber":
                    float(dish["fiber"] or 0)
                    * float(quantity),

                "quantity": quantity,

                "source": "app",

                "status": "logged"
            }
        )

    return {

        "success": True,

        "message": "Meal Logged Successfully"

    }