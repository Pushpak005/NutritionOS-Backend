from app.core.context.models import Context


# ==========================================
# Meal Recommendation Policy
# ==========================================

def can_recommend_current_meal(
    context: Context
) -> bool:

    # ==========================================
    # Late Night Guard
    #
    # The current prototype has no dedicated
    # late-night meal category.
    #
    # Do not silently convert Late Night into
    # another meal such as Dinner.
    # ==========================================

    meal_window = str(
        context.meal_window or ""
    ).strip().lower()

    if meal_window == "late night":

        return False

    # ==========================================
    # Meal Completion Guard
    #
    # A normal full-meal recommendation should
    # not be generated when the current meal has
    # already been logged today.
    # ==========================================

    logged_meals = {

        "breakfast":
            context.breakfast_logged,

        "lunch":
            context.lunch_logged,

        "dinner":
            context.dinner_logged

    }

    if meal_window in logged_meals:

        return not bool(
            logged_meals[meal_window]
        )

    # ==========================================
    # Snack
    #
    # The current Context model does not yet
    # contain snack_logged.
    #
    # Therefore Snack remains eligible here.
    # ==========================================

    return True