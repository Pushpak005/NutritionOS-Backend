from typing import Dict


# ==========================================================
# NutritionOS Recommendation Engine
# ==========================================================
#
# Continuous nutrition-aware recommendation scoring.
#
# Final score:
#     0 - 100
#
# Components:
#
# Calories Fit       = 20
# Protein Fit        = 25
# Goal Fit           = 20
# Healthy Score      = 15
# Macro / Fiber Fit  = 10
# Budget Fit         = 5
# Restaurant Rating  = 5
#
# IMPORTANT:
#
# The previous version used many hard thresholds.
# That caused multiple dishes to receive identical scores.
#
# This version uses continuous scoring wherever possible.
#
# Example:
#
# 616 kcal vs 664 kcal
# 625 kcal vs 664 kcal
# 658 kcal vs 664 kcal
# 665 kcal vs 664 kcal
#
# will no longer automatically receive identical calorie points.
# ==========================================================


# ==========================================================
# Safe Numeric Helper
# ==========================================================

def _number(value, default=0.0) -> float:

    try:

        return float(
            value if value is not None else default
        )

    except (TypeError, ValueError):

        return float(default)


# ==========================================================
# Safe Text Helper
# ==========================================================

def _text(value) -> str:

    if value is None:

        return ""

    return str(value).strip().lower()


# ==========================================================
# Clamp Helper
# ==========================================================

def _clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:

    return max(
        minimum,
        min(value, maximum)
    )


# ==========================================================
# Calories Fit — 20 Points
# ==========================================================
#
# Continuous Gaussian-style fit.
#
# Perfect match:
#     20 points
#
# Small difference:
#     small penalty
#
# Large difference:
#     progressively lower score
#
# This avoids:
#
# <= 50  -> 20
# <= 100 -> 18
#
# style jumps.
# ==========================================================

def _calculate_calorie_score(
    target_calories: float,
    calories: float
) -> float:

    if target_calories <= 0 or calories <= 0:

        return 0.0

    difference = abs(
        calories - target_calories
    )

    # ------------------------------------------------------
    # Scale relative to meal target.
    #
    # 20% of target is treated as a meaningful deviation.
    # ------------------------------------------------------

    tolerance = max(
        target_calories * 0.20,
        100.0
    )

    score = 20.0 * (
        1.0
        -
        (difference / tolerance)
    )

    return _clamp(
        score,
        0.0,
        20.0
    )


# ==========================================================
# Protein Fit — 25 Points
# ==========================================================
#
# Protein should help close the remaining protein gap.
#
# Ideal behaviour:
#
#     25-40% of remaining gap
#         -> useful
#
#     40-80%
#         -> strong
#
#     80-100%
#         -> very strong
#
#     >100%
#         -> still useful, but diminishing return
#
# We deliberately avoid giving automatic maximum points
# merely because protein is above a threshold.
# ==========================================================

def _calculate_protein_score(
    user: Dict,
    protein: float
) -> float:

    nutrition_state = user.get("nutrition_state")

    remaining_protein = _number(
        nutrition_state.remaining_protein
        if nutrition_state
        else 0
    )

    goal = _text(
        user.get("goal")
    )

    if protein <= 0:

        return 0.0

    # ------------------------------------------------------
    # If no protein gap exists, avoid rewarding excessive
    # protein simply for being high.
    # ------------------------------------------------------

    if remaining_protein <= 0:

        if goal in (
            "muscle gain",
            "weight gain"
        ):

            return _clamp(
                protein / 40.0 * 25.0,
                0.0,
                25.0
            )

        return _clamp(
            protein / 30.0 * 20.0,
            0.0,
            20.0
        )

    ratio = (
        protein /
        remaining_protein
    )

    # ------------------------------------------------------
    # Best range is approximately 25%-100% of remaining
    # protein requirement.
    #
    # Use a smooth triangular-style response.
    # ------------------------------------------------------

    if ratio <= 1.0:

        score = 25.0 * (
            ratio / 0.80
        )

        # Cap near full score around 80% completion.
        score = min(
            score,
            25.0
        )

    else:

        # Diminishing returns after the gap is covered.
        excess = ratio - 1.0

        score = 25.0 * (
            1.0
            -
            min(
                excess * 0.45,
                0.65
            )
        )

    # ------------------------------------------------------
    # Avoid rewarding extremely large protein meals
    # equally to appropriately sized meals.
    # ------------------------------------------------------

    if ratio > 2.0:

        score -= min(
            (ratio - 2.0) * 4.0,
            6.0
        )

    return _clamp(
        score,
        0.0,
        25.0
    )


# ==========================================================
# Goal Fit — 20 Points
# ==========================================================
#
# Goal fit is intentionally smooth.
#
# Maintain:
#     balanced nutrition
#
# Weight loss:
#     reasonable calories + protein + fiber
#
# Muscle / weight gain:
#     protein + sufficient calories
# ==========================================================

def _calculate_goal_score(
    user: Dict,
    dish: Dict
) -> float:

    goal = _text(
        user.get("goal")
    )

    calories = _number(
        dish.get("calories")
    )

    protein = _number(
        dish.get("protein")
    )

    fiber = _number(
        dish.get("fiber")
    )

    fat = _number(
        dish.get("fat")
    )

    carbs = _number(
        dish.get("carbs")
    )

    target_calories = _number(
        user.get("meal_target_calories")
    )

    if target_calories <= 0:

        target_calories = _number(
            user.get("daily_calories")
        )

    # ------------------------------------------------------
    # Weight / Muscle Gain
    # ------------------------------------------------------

    if goal in (
        "muscle gain",
        "weight gain"
    ):

        protein_component = _clamp(
            protein / 40.0,
            0.0,
            1.0
        )

        calorie_component = 1.0

        if target_calories > 0:

            calorie_ratio = (
                calories /
                target_calories
            )

            calorie_component = _clamp(
                1.0 -
                abs(
                    calorie_ratio - 1.0
                ),
                0.0,
                1.0
            )

        return (
            protein_component * 12.0
            +
            calorie_component * 6.0
            +
            _clamp(
                fiber / 10.0,
                0.0,
                1.0
            ) * 2.0
        )

    # ------------------------------------------------------
    # Weight Loss
    # ------------------------------------------------------

    if goal == "weight loss":

        calorie_component = 1.0

        if target_calories > 0:

            ratio = (
                calories /
                target_calories
            )

            if ratio <= 1.0:

                calorie_component = _clamp(
                    ratio,
                    0.0,
                    1.0
                )

            else:

                calorie_component = _clamp(
                    1.0 -
                    (
                        ratio - 1.0
                    ) * 2.0,
                    0.0,
                    1.0
                )

        protein_component = _clamp(
            protein / 30.0,
            0.0,
            1.0
        )

        fiber_component = _clamp(
            fiber / 10.0,
            0.0,
            1.0
        )

        fat_component = _clamp(
            1.0 -
            max(fat - 15.0, 0.0) / 20.0,
            0.0,
            1.0
        )

        return (
            calorie_component * 7.0
            +
            protein_component * 7.0
            +
            fiber_component * 4.0
            +
            fat_component * 2.0
        )

    # ------------------------------------------------------
    # Maintain / Default
    # ------------------------------------------------------

    calorie_component = 1.0

    if target_calories > 0:

        calorie_ratio = (
            calories /
            target_calories
        )

        calorie_component = _clamp(
            1.0 -
            abs(
                calorie_ratio - 1.0
            ),
            0.0,
            1.0
        )

    protein_component = _clamp(
        protein / 30.0,
        0.0,
        1.0
    )

    fiber_component = _clamp(
        fiber / 10.0,
        0.0,
        1.0
    )

    macro_component = 1.0

    if carbs > 0:

        macro_component = _clamp(
            1.0 -
            abs(
                carbs - 55.0
            ) / 55.0,
            0.0,
            1.0
        )

    return (
        calorie_component * 7.0
        +
        protein_component * 7.0
        +
        fiber_component * 3.0
        +
        macro_component * 3.0
    )


# ==========================================================
# Healthy Score — 15 Points
# ==========================================================

def _calculate_healthy_score(
    dish: Dict
) -> float:

    healthy_score = _number(
        dish.get("healthy_score")
    )

    if healthy_score <= 0:

        # Prototype fallback.
        return 7.5

    return _clamp(
        (
            healthy_score /
            100.0
        ) * 15.0,
        0.0,
        15.0
    )


# ==========================================================
# Macro / Fiber Balance — 10 Points
# ==========================================================
#
# Continuous rather than threshold-based.
# ==========================================================

def _calculate_macro_score(
    user: Dict,
    dish: Dict
) -> float:

    protein = _number(
        dish.get("protein")
    )

    fiber = _number(
        dish.get("fiber")
    )

    fat = _number(
        dish.get("fat")
    )

    carbs = _number(
        dish.get("carbs")
    )

    goal = _text(
        user.get("goal")
    )

    # ------------------------------------------------------
    # Protein
    # ------------------------------------------------------

    protein_score = _clamp(
        protein / 30.0,
        0.0,
        1.0
    ) * 3.0

    # ------------------------------------------------------
    # Fiber
    # ------------------------------------------------------

    fiber_score = _clamp(
        fiber / 10.0,
        0.0,
        1.0
    ) * 3.0

    # ------------------------------------------------------
    # Fat
    # ------------------------------------------------------

    if fat <= 15:

        fat_score = 2.0

    else:

        fat_score = _clamp(
            2.0 -
            (
                (fat - 15.0) /
                15.0
            ) * 2.0,
            0.0,
            2.0
        )

    # ------------------------------------------------------
    # Carbohydrate Fit
    # ------------------------------------------------------

    if goal in (
        "muscle gain",
        "weight gain"
    ):

        ideal_carbs = 60.0

    elif goal == "weight loss":

        ideal_carbs = 45.0

    else:

        ideal_carbs = 55.0

    carb_score = _clamp(
        2.0 -
        (
            abs(
                carbs -
                ideal_carbs
            ) /
            50.0
        ) * 2.0,
        0.0,
        2.0
    )

    return _clamp(
        protein_score
        +
        fiber_score
        +
        fat_score
        +
        carb_score,
        0.0,
        10.0
    )


# ==========================================================
# Budget Fit — 5 Points
# ==========================================================

def _calculate_budget_score(
    user: Dict,
    dish: Dict
) -> float:

    budget = _number(
        user.get("daily_budget")
    )

    price = _number(
        dish.get("price")
    )

    if budget <= 0 or price <= 0:

        return 2.5

    ratio = (
        price /
        budget
    )

    if ratio <= 1.0:

        # Best score inside budget.
        return 5.0 - (
            ratio * 0.5
        )

    # Gradual penalty above budget.
    return _clamp(
        5.0 -
        (
            ratio - 1.0
        ) * 10.0,
        0.0,
        5.0
    )


# ==========================================================
# Restaurant Rating — 5 Points
# ==========================================================

def _calculate_rating_score(
    dish: Dict
) -> float:

    rating = _number(
        dish.get("rating")
    )

    if rating <= 0:

        return 2.5

    # 3.0 rating -> 0
    # 5.0 rating -> 5
    score = (
        rating - 3.0
    ) / 2.0 * 5.0

    return _clamp(
        score,
        0.0,
        5.0
    )


# ==========================================================
# Nutrition Gap Adjustment
# ==========================================================
#
# Kept deliberately small.
#
# The main score should determine ranking.
# ==========================================================

def _calculate_gap_adjustment(
    user: Dict,
    dish: Dict
) -> float:

    remaining = user.get(
        "remaining"
    ) or {}

    remaining_protein = _number(
        remaining.get("protein")
    )

    remaining_fiber = _number(
        remaining.get("fiber")
    )

    remaining_calories = _number(
        remaining.get("calories")
    )

    protein = _number(
        dish.get("protein")
    )

    fiber = _number(
        dish.get("fiber")
    )

    calories = _number(
        dish.get("calories")
    )

    adjustment = 0.0

    # ------------------------------------------------------
    # Protein gap
    # ------------------------------------------------------

    if (
        remaining_protein > 0
        and protein > 0
    ):

        ratio = (
            protein /
            remaining_protein
        )

        if 0.25 <= ratio <= 1.0:

            adjustment += 1.0

        elif ratio > 2.0:

            adjustment -= 1.5

    # ------------------------------------------------------
    # Fiber gap
    # ------------------------------------------------------

    if (
        remaining_fiber > 0
        and fiber > 0
    ):

        ratio = (
            fiber /
            remaining_fiber
        )

        if ratio >= 0.25:

            adjustment += 0.5

    # ------------------------------------------------------
    # Remaining calorie protection
    # ------------------------------------------------------

    if (
        remaining_calories > 0
        and calories > remaining_calories
    ):

        overshoot = (
            calories -
            remaining_calories
        )

        adjustment -= _clamp(
            overshoot / 100.0,
            0.5,
            3.0
        )

    return adjustment


# ==========================================================
# Main Nutrition Score
# ==========================================================

def calculate_nutrition_score(
    user: Dict,
    dish: Dict
) -> int:

    user = dict(user)
    dish = dict(dish)

    # ======================================================
    # Meal Target
    # ======================================================

    target_calories = _number(
        user.get(
            "meal_target_calories"
        )
    )

    if target_calories <= 0:

        target_calories = _number(
            user.get(
                "daily_calories"
            )
        )

    # ======================================================
    # Component Scores
    # ======================================================

    calorie_score = (
        _calculate_calorie_score(
            target_calories,
            _number(
                dish.get("calories")
            )
        )
    )

    protein_score = (
        _calculate_protein_score(
            user,
            _number(
                dish.get("protein")
            )
        )
    )

    goal_score = (
        _calculate_goal_score(
            user,
            dish
        )
    )

    healthy_score = (
        _calculate_healthy_score(
            dish
        )
    )

    macro_score = (
        _calculate_macro_score(
            user,
            dish
        )
    )

    budget_score = (
        _calculate_budget_score(
            user,
            dish
        )
    )

    rating_score = (
        _calculate_rating_score(
            dish
        )
    )

    # ======================================================
    # Base Score
    # ======================================================

    score = (

        calorie_score
        +
        protein_score
        +
        goal_score
        +
        healthy_score
        +
        macro_score
        +
        budget_score
        +
        rating_score

    )

    # ======================================================
    # Small Contextual Adjustment
    # ======================================================

    score += _calculate_gap_adjustment(
        user,
        dish
    )

    # ======================================================
    # Final Bounds
    # ======================================================

    return max(
        0,
        min(
            round(score),
            100
        )
    )


# ==========================================================
# Dynamic Recommendation Explanation
# ==========================================================

def get_recommendation_reasons(
    user: Dict,
    dish: Dict
) -> list:

    reasons = []

    goal = _text(
        user.get("goal")
    )

    remaining = user.get(
        "remaining"
    ) or {}

    remaining_protein = _number(
        remaining.get("protein")
    )

    remaining_calories = _number(
        remaining.get("calories")
    )

    protein = _number(
        dish.get("protein")
    )

    calories = _number(
        dish.get("calories")
    )

    fiber = _number(
        dish.get("fiber")
    )

    healthy_score = _number(
        dish.get("healthy_score")
    )

    price = _number(
        dish.get("price")
    )

    budget = _number(
        user.get("daily_budget")
    )

    rating = _number(
        dish.get("rating")
    )

    # ======================================================
    # Protein
    # ======================================================

    if (
        remaining_protein > 0
        and protein > 0
    ):

        ratio = (
            protein /
            remaining_protein
        )

        if 0.25 <= ratio <= 1.0:

            reasons.append({

                "type": "protein",

                "title":
                    "Fits your protein gap",

                "text": (
                    f"You have about "
                    f"{round(remaining_protein)}g protein "
                    f"remaining, and this meal provides "
                    f"{round(protein)}g."
                )

            })

        elif ratio > 1.50:

            reasons.append({

                "type": "protein",

                "title":
                    "Very high protein",

                "text": (
                    f"This meal provides "
                    f"{round(protein)}g protein, which is "
                    f"more than your current remaining "
                    f"protein requirement."
                )

            })

        else:

            reasons.append({

                "type": "protein",

                "title":
                    "Contributes to your protein target",

                "text": (
                    f"This meal provides "
                    f"{round(protein)}g protein toward "
                    f"your remaining "
                    f"{round(remaining_protein)}g."
                )

            })

    # ======================================================
    # Calories
    # ======================================================

    if (
        remaining_calories > 0
        and calories > 0
    ):

        if calories <= remaining_calories:

            reasons.append({

                "type": "calories",

                "title":
                    "Fits your remaining calories",

                "text": (
                    f"{round(calories)} kcal fits within "
                    f"your remaining "
                    f"{round(remaining_calories)} kcal."
                )

            })

        else:

            reasons.append({

                "type": "calories",

                "title":
                    "Higher than your remaining calories",

                "text": (
                    f"This meal has "
                    f"{round(calories)} kcal versus "
                    f"{round(remaining_calories)} kcal "
                    f"remaining today."
                )

            })

    # ======================================================
    # Goal
    # ======================================================

    if goal in (
        "muscle gain",
        "weight gain"
    ):

        if protein >= 25:

            reasons.append({

                "type": "goal",

                "title":
                    "Supports your muscle goal",

                "text": (
                    "Its protein and calorie profile "
                    "supports your current "
                    "muscle-building goal."
                )

            })

    elif goal == "weight loss":

        reasons.append({

            "type": "goal",

            "title":
                "Fits your weight-loss goal",

            "text": (
                "Its calorie and nutrition profile "
                "is evaluated against your "
                "weight-loss needs."
            )

        })

    elif goal == "maintain":

        reasons.append({

            "type": "goal",

            "title":
                "Fits your maintenance goal",

            "text": (
                "Its calories and nutrition profile "
                "are evaluated against your "
                "maintenance needs."
            )

        })

    # ======================================================
    # Healthy Score
    # ======================================================

    if healthy_score >= 90:

        reasons.append({

            "type": "health",

            "title":
                "Excellent healthy score",

            "text": (
                f"This dish has a healthy score "
                f"of {round(healthy_score)}/100."
            )

        })

    elif healthy_score >= 75:

        reasons.append({

            "type": "health",

            "title":
                "Good healthy score",

            "text": (
                f"This dish has a healthy score "
                f"of {round(healthy_score)}/100."
            )

        })

    # ======================================================
    # Fiber
    # ======================================================

    if fiber >= 8:

        reasons.append({

            "type": "fiber",

            "title":
                "Good fiber contribution",

            "text": (
                f"This meal provides around "
                f"{round(fiber)}g of fiber."
            )

        })

    elif fiber >= 5:

        reasons.append({

            "type": "fiber",

            "title":
                "Provides useful fiber",

            "text": (
                f"This meal provides around "
                f"{round(fiber)}g of fiber."
            )

        })

    # ======================================================
    # Budget
    # ======================================================

    if (
        budget > 0
        and price > 0
    ):

        if price <= budget:

            reasons.append({

                "type": "budget",

                "title":
                    "Within your budget",

                "text": (
                    f"₹{round(price)} is within "
                    f"your ₹{round(budget)} daily budget."
                )

            })

        else:

            reasons.append({

                "type": "budget",

                "title":
                    "Above your budget",

                "text": (
                    f"₹{round(price)} is above "
                    f"your ₹{round(budget)} daily budget."
                )

            })

    # ======================================================
    # Restaurant Rating
    # ======================================================

    if rating >= 4.5:

        reasons.append({

            "type": "restaurant",

            "title":
                "Highly rated restaurant",

            "text": (
                f"The restaurant is rated "
                f"{rating:.1f}/5."
            )

        })

    return reasons