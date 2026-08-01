from sqlalchemy import text
from app.database import engine


def get_profile(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    name,
                    email,
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    goal,
                    activity_level,
                    daily_budget,
                    diet_preferences
                FROM users
                WHERE id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).fetchone()

    if result is None:
        return None

    return dict(result._mapping)


def update_profile(user_id: int, data: dict):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE users
                SET
                    name = :name,
                    age = :age,
                    gender = :gender,
                    height_cm = :height_cm,
                    weight_kg = :weight_kg,
                    goal = :goal,
                    activity_level = :activity_level,
                    daily_budget = :daily_budget,
                    diet_preferences = :diet_preferences
                WHERE id = :user_id
            """),
            {
                "user_id": user_id,
                **data
            }
        )

    return get_profile(user_id)