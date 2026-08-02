from sqlalchemy import text

from app.database import engine
from app.services.nutrition_engine import calculate_nutrition


# ==========================================
# Get Profile
# ==========================================

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
                    diet_preferences,

                    bmi,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber,

                    target_weight,
                    allergies,
                    health_conditions

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


# ==========================================
# Update Profile
# ==========================================

def update_profile(user_id: int, data: dict):

    with engine.begin() as conn:

        # -----------------------------
        # Update profile
        # -----------------------------

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
                    diet_preferences = :diet_preferences,
                    target_weight = :target_weight,
                    allergies = :allergies,
                    health_conditions = :health_conditions
                WHERE id = :user_id
            """),
            {
                "user_id": user_id,
                **data
            }
        )

        # -----------------------------
        # Fetch latest values
        # -----------------------------

        profile = conn.execute(
            text("""
                SELECT
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    goal,
                    activity_level
                FROM users
                WHERE id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).fetchone()

        profile = dict(profile._mapping)

        # -----------------------------
        # Run Nutrition Engine
        # -----------------------------

        nutrition = calculate_nutrition(profile)

        # -----------------------------
        # Save calculated nutrition
        # -----------------------------

        conn.execute(
            text("""
                UPDATE users
                SET
                    bmi = :bmi,
                    daily_calories = :daily_calories,
                    daily_protein = :daily_protein,
                    daily_carbs = :daily_carbs,
                    daily_fat = :daily_fat,
                    daily_fiber = :daily_fiber
                WHERE id = :user_id
            """),
            {
                "user_id": user_id,
                **nutrition
            }
        )

    return get_profile(user_id)