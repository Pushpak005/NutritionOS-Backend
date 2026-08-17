from dataclasses import dataclass

from app.core.context.models import Context


@dataclass
class NutritionState:

    # ==========================================
    # Remaining Nutrition
    # ==========================================

    remaining_calories: float

    remaining_protein: float

    remaining_carbs: float

    remaining_fat: float

    remaining_fiber: float

    # ==========================================
    # Meal / User State
    # ==========================================

    meal_window: str

    goal: str


def build_nutrition_state(
    context: Context
) -> NutritionState:

    return NutritionState(

        # --------------------------------------
        # Remaining Nutrition
        # --------------------------------------

        remaining_calories=
            context.remaining_calories,

        remaining_protein=
            context.remaining_protein,

        remaining_carbs=
            context.remaining_carbs,

        remaining_fat=
            context.remaining_fat,

        remaining_fiber=
            context.remaining_fiber,

        # --------------------------------------
        # Meal / User State
        # --------------------------------------

        meal_window=
            context.meal_window,

        goal=
            context.goal

    )