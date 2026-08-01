from sqlalchemy import text
from app.database import engine


def log_meal(user_id, menu_item_id, meal_type, quantity):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO meals
                (
                    user_id,
                    menu_item_id,
                    meal_type,
                    quantity
                )
                VALUES
                (
                    :user_id,
                    :menu_item_id,
                    :meal_type,
                    :quantity
                )
            """),
            {
                "user_id": user_id,
                "menu_item_id": menu_item_id,
                "meal_type": meal_type,
                "quantity": quantity
            }
        )

    return {
        "success": True,
        "message": "Meal Logged Successfully"
    }