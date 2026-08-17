from app.core.context.models import Context
from app.core.context.time_context import get_current_meal_window

from app.core.providers.manual_provider import ManualProvider


class ContextFactory:

    def __init__(self, provider=None):

        # ==========================================
        # Default Provider
        # ==========================================

        self.provider = provider or ManualProvider()

    # ==========================================
    # Build User Context
    # ==========================================

    def build(self, user_id: int) -> Context:

        # ==========================================
        # User
        # ==========================================

        user = self.provider.get_user(
            user_id
        )

        # ==========================================
        # Nutrition
        # ==========================================

        nutrition = self.provider.get_nutrition(
            user_id
        )

        # ==========================================
        # Activity
        # ==========================================

        activity = self.provider.get_activity(
            user_id
        )

        # ==========================================
        # Device
        # ==========================================

        device = self.provider.get_device(
            user_id
        )

        # ==========================================
        # Safe Numeric Values
        # ==========================================

        daily_calories = float(
            nutrition["daily_calories"] or 0
        )

        consumed_calories = float(
            nutrition["consumed_calories"] or 0
        )

        daily_protein = float(
            nutrition["daily_protein"] or 0
        )

        consumed_protein = float(
            nutrition["consumed_protein"] or 0
        )

        daily_carbs = float(
            nutrition["daily_carbs"] or 0
        )

        consumed_carbs = float(
            nutrition["consumed_carbs"] or 0
        )

        daily_fat = float(
            nutrition["daily_fat"] or 0
        )

        consumed_fat = float(
            nutrition["consumed_fat"] or 0
        )

        daily_fiber = float(
            nutrition["daily_fiber"] or 0
        )

        consumed_fiber = float(
            nutrition["consumed_fiber"] or 0
        )

        # ==========================================
        # Build Context
        # ==========================================

        return Context(

            # --------------------------------------
            # User
            # --------------------------------------

            user_id=user["user_id"],

            goal=user["goal"],

            # --------------------------------------
            # Time
            # --------------------------------------

            meal_window=get_current_meal_window(),

            # --------------------------------------
            # Nutrition
            # --------------------------------------

            remaining_calories=max(
                daily_calories - consumed_calories,
                0
            ),

            remaining_protein=max(
                daily_protein - consumed_protein,
                0
            ),

            remaining_carbs=max(
                daily_carbs - consumed_carbs,
                0
            ),

            remaining_fat=max(
                daily_fat - consumed_fat,
                0
            ),

            remaining_fiber=max(
                daily_fiber - consumed_fiber,
                0
            ),

            # --------------------------------------
            # Activity
            # --------------------------------------

            steps=int(
                activity.get(
                    "steps",
                    0
                ) or 0
            ),

            calories_burned=float(
                activity.get(
                    "calories_burned",
                    0
                ) or 0
            ),

            workout_today=bool(
                activity.get(
                    "workout_today",
                    False
                )
            ),

            # --------------------------------------
            # Meal State
            # --------------------------------------

            breakfast_logged=bool(
                activity.get(
                    "breakfast_logged",
                    False
                )
            ),

            lunch_logged=bool(
                activity.get(
                    "lunch_logged",
                    False
                )
            ),

            dinner_logged=bool(
                activity.get(
                    "dinner_logged",
                    False
                )
            ),

            # --------------------------------------
            # Device
            # --------------------------------------

            health_connected=bool(
                device.get(
                    "health_connected",
                    False
                )
            )

        )