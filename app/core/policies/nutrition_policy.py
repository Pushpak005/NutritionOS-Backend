from app.core.state.nutrition_state import NutritionState


# ==========================================
# Nutrition Completion Policy
# ==========================================

def can_recommend_full_meal(
    state: NutritionState
) -> bool:

    # ==========================================
    # Nutrition Completion Guard
    #
    # If the user has essentially completed
    # today's calorie target and has already
    # reached the protein target, do not
    # recommend another normal full meal.
    # ==========================================

    if (
        state.remaining_calories <= 100
        and state.remaining_protein <= 0
    ):
        return False

    return True