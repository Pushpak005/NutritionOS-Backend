from sqlalchemy import text

from app.database import engine
from app.core.contracts.provider_contract import ProviderContract


class ManualProvider(ProviderContract):

    """
    Manual Provider

    Current Source:
        - User Profile
        - Meal Logs
        - Database

    Future:
        - Android Health Connect
        - Samsung Health
        - Google Fit
    """

    # ==========================================
    # User
    # ==========================================

    def get_user(self, user_id: int):

        with engine.connect() as conn:

            user = conn.execute(

                text("""
                    SELECT
                        id,
                        goal
                    FROM users
                    WHERE id = :id
                """),

                {
                    "id": user_id
                }

            ).mappings().first()

        if not user:

            raise Exception("User not found.")

        return {

            "user_id": user["id"],

            "goal": user["goal"]

        }

    # ==========================================
    # Nutrition
    # ==========================================

    def get_nutrition(self, user_id: int):

        with engine.connect() as conn:

            nutrition = conn.execute(

                text("""
                    SELECT

                        u.daily_calories,
                        u.daily_protein,
                        u.daily_carbs,
                        u.daily_fat,
                        u.daily_fiber,

                        COALESCE(
                            SUM(ml.calories),
                            0
                        ) AS consumed_calories,

                        COALESCE(
                            SUM(ml.protein),
                            0
                        ) AS consumed_protein,

                        COALESCE(
                            SUM(ml.carbs),
                            0
                        ) AS consumed_carbs,

                        COALESCE(
                            SUM(ml.fat),
                            0
                        ) AS consumed_fat,

                        COALESCE(
                            SUM(ml.fiber),
                            0
                        ) AS consumed_fiber

                    FROM users u

                    LEFT JOIN meal_logs ml

                        ON u.id = ml.user_id

                        AND DATE(ml.eaten_at) = CURRENT_DATE

                    WHERE u.id = :id

                    GROUP BY
                        u.daily_calories,
                        u.daily_protein,
                        u.daily_carbs,
                        u.daily_fat,
                        u.daily_fiber
                """),

                {
                    "id": user_id
                }

            ).mappings().first()

        if not nutrition:

            raise Exception(
                "Nutrition query returned nothing."
            )

        return {

            "daily_calories":
                nutrition["daily_calories"],

            "daily_protein":
                nutrition["daily_protein"],

            "daily_carbs":
                nutrition["daily_carbs"],

            "daily_fat":
                nutrition["daily_fat"],

            "daily_fiber":
                nutrition["daily_fiber"],

            "consumed_calories":
                nutrition["consumed_calories"],

            "consumed_protein":
                nutrition["consumed_protein"],

            "consumed_carbs":
                nutrition["consumed_carbs"],

            "consumed_fat":
                nutrition["consumed_fat"],

            "consumed_fiber":
                nutrition["consumed_fiber"]

        }

    # ==========================================
    # Activity + Meal State
    # ==========================================

    def get_activity(self, user_id: int):

        with engine.connect() as conn:

            meal_state = conn.execute(

                text("""
                    SELECT

                        COALESCE(
                            BOOL_OR(
                                LOWER(meal_type) = 'breakfast'
                            ),
                            FALSE
                        ) AS breakfast_logged,

                        COALESCE(
                            BOOL_OR(
                                LOWER(meal_type) = 'lunch'
                            ),
                            FALSE
                        ) AS lunch_logged,

                        COALESCE(
                            BOOL_OR(
                                LOWER(meal_type) = 'dinner'
                            ),
                            FALSE
                        ) AS dinner_logged

                    FROM meal_logs

                    WHERE

                        user_id = :id

                        AND DATE(eaten_at) = CURRENT_DATE
                """),

                {
                    "id": user_id
                }

            ).mappings().first()

        return {

            # ----------------------------------
            # Current prototype activity
            # ----------------------------------

            "steps": 0,

            "calories_burned": 0,

            "workout_today": False,

            # ----------------------------------
            # Real meal state
            # ----------------------------------

            "breakfast_logged": bool(
                meal_state["breakfast_logged"]
            ),

            "lunch_logged": bool(
                meal_state["lunch_logged"]
            ),

            "dinner_logged": bool(
                meal_state["dinner_logged"]
            )

        }

    # ==========================================
    # Device
    # ==========================================

    def get_device(self, user_id: int):

        """
        Current prototype:

            Health Connect = unavailable

        Future:

            Android
                ↓
            Health Connect
                ↓
            Device status
        """

        return {

            "health_connected": False

        }