from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(tags=["Restaurant Details"])


@router.get("/restaurant/{restaurant_id}")

def get_restaurant(restaurant_id: int):

    with engine.connect() as conn:

        restaurant = conn.execute(

            text("""

                SELECT *

                FROM restaurants

                WHERE restaurant_id = :restaurant_id

            """),

            {

                "restaurant_id": restaurant_id

            }

        ).mappings().first()

        if not restaurant:

            return {

                "message": "Restaurant not found"

            }

        menu = conn.execute(

            text("""

                SELECT *

                FROM menu_items

                WHERE restaurant_id = :restaurant_id

                ORDER BY healthy_score DESC

            """),

            {

                "restaurant_id": restaurant_id

            }

        ).mappings().all()

    return {

        "restaurant": dict(restaurant),

        "menu": [dict(x) for x in menu]

    }