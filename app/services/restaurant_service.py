from sqlalchemy import text
from app.database import engine


def get_restaurants():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    restaurant_id,
                    restaurant_name,
                    area,
                    rating,
                    delivery_time
                FROM restaurants
                ORDER BY rating DESC
            """)
        ).fetchall()

    return [dict(row._mapping) for row in result]