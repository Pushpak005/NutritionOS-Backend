from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    tags=["Dish"]
)


@router.get("/dish/{dish_id}")
def get_dish(dish_id: int):

    with engine.connect() as conn:

        dish = conn.execute(

            text("""

                SELECT

                    m.*,

                    r.restaurant_name,

                    r.area,

                    r.rating,

                    r.delivery_time

                FROM menu_items m

                JOIN restaurants r

                    ON r.restaurant_id = m.restaurant_id

                WHERE

                    m.id = :dish_id

            """),

            {
                "dish_id": dish_id
            }

        ).mappings().first()

    if not dish:

        return {

            "message": "Dish not found"

        }

    return dict(dish)