from dataclasses import dataclass

from app.core.context.models import Context
from app.core.policies.meal_policy import (
    can_recommend_current_meal
)
from app.core.policies.nutrition_policy import (
    can_recommend_full_meal
)
from app.core.state.nutrition_state import (
    build_nutrition_state
)


# ==========================================
# NutritionOS Action Decision
# ==========================================


@dataclass(frozen=True)
class ActionDecision:

    allowed: bool
    reason: str
    nutrition_complete: bool


# ==========================================
# Decision Reasons
# ==========================================


ACTION_ALLOWED = (
    "MEAL_RECOMMENDATION_ALLOWED"
)

ACTION_BLOCKED_NO_CONTEXT = (
    "NO_CONTEXT"
)

ACTION_BLOCKED_MEAL = (
    "CURRENT_MEAL_NOT_ELIGIBLE"
)

ACTION_BLOCKED_NUTRITION = (
    "NUTRITION_TARGET_COMPLETED"
)


# ==========================================
# NutritionOS Action Policy
# ==========================================
#
# This is the single deterministic gateway
# for deciding whether a normal meal
# recommendation action is currently allowed.
#
# The policy layer answers:
#
# "Should NutritionOS recommend a normal
#  full meal right now?"
#
# It does NOT decide which dish is best.
#
# Ranking remains the responsibility of the
# recommendation engine.
# ==========================================


def evaluate_meal_action(
    context: Context
) -> ActionDecision:

    # ==========================================
    # Safety: Context Required
    # ==========================================

    if context is None:

        return ActionDecision(
            allowed=False,
            reason=ACTION_BLOCKED_NO_CONTEXT,
            nutrition_complete=False
        )

    # ==========================================
    # Build Central Nutrition State
    #
    # The same centralized NutritionState is
    # used by the nutrition policy and the
    # recommendation layer.
    # ==========================================

    nutrition_state = (
        build_nutrition_state(
            context
        )
    )

    # ==========================================
    # Nutrition Completion State
    #
    # IMPORTANT:
    #
    # Nutrition completion is owned by the
    # nutrition policy.
    #
    # Do NOT duplicate the calorie/protein
    # completion rule in dashboard or other
    # service layers.
    # ==========================================

    nutrition_complete = not can_recommend_full_meal(
        nutrition_state
    )

    # ==========================================
    # Meal Policy
    #
    # Checks:
    #
    # - current meal window
    # - late-night restriction
    # - whether the current meal has already
    #   been logged
    # ==========================================

    if not can_recommend_current_meal(
        context
    ):

        return ActionDecision(
            allowed=False,
            reason=ACTION_BLOCKED_MEAL,
            nutrition_complete=nutrition_complete
        )

    # ==========================================
    # Nutrition Policy
    #
    # Checks whether the user has effectively
    # completed today's nutrition requirement.
    # ==========================================

    if nutrition_complete:

        return ActionDecision(
            allowed=False,
            reason=ACTION_BLOCKED_NUTRITION,
            nutrition_complete=True
        )

    # ==========================================
    # All deterministic policies passed.
    # ==========================================

    return ActionDecision(
        allowed=True,
        reason=ACTION_ALLOWED,
        nutrition_complete=False
    )


# ==========================================
# Backward-Compatible Boolean Gateway
# ==========================================


def can_recommend_meal(
    context: Context
) -> bool:

    return evaluate_meal_action(
        context
    ).allowed