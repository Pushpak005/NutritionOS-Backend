from dataclasses import dataclass


# ==========================================
# NutritionOS Core Context
# ==========================================

@dataclass
class Context:

    # -------------------------
    # User
    # -------------------------

    user_id: int

    goal: str

    # -------------------------
    # Time
    # -------------------------

    meal_window: str

    # -------------------------
    # Nutrition
    # -------------------------

    remaining_calories: int

    remaining_protein: int

    remaining_carbs: int

    remaining_fat: int

    remaining_fiber: int

    # -------------------------
    # Activity
    # -------------------------

    steps: int

    calories_burned: int

    workout_today: bool

    # -------------------------
    # Meals
    # -------------------------

    breakfast_logged: bool

    lunch_logged: bool

    dinner_logged: bool

    # -------------------------
    # Device
    # -------------------------

    health_connected: bool