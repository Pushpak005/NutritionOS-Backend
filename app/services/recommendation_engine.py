from typing import Dict


def calculate_nutrition_score(
    user: Dict,
    dish: Dict
) -> float:

    score = 0

    # -----------------------
    # Safe Values
    # -----------------------

    target_calories = (
    user.get("meal_target_calories")
    or user.get("daily_calories")
    or 0)

    calories = dish.get("calories") or 0

    protein = float(dish.get("protein") or 0)

    fat = float(dish.get("fat") or 0)

    price = float(dish.get("price") or 0)

    rating = float(dish.get("rating") or 0)

    goal = (user.get("goal") or "").lower()

    # -----------------------
    # Calories
    # -----------------------

    difference = abs(target_calories - calories)

    if difference <= 100:
        score += 30

    elif difference <= 250:
        score += 20

    elif difference <= 500:
        score += 10

    # -----------------------
    # Protein
    # -----------------------

    if protein >= 40:
        score += 30

    elif protein >= 25:
        score += 25

    elif protein >= 15:
        score += 15

    # -----------------------
    # Goal Based Scoring
    # -----------------------

    if goal == "weight loss":

        if fat <= 15:
            score += 20

        elif fat <= 25:
            score += 10

    elif goal == "weight gain":

        if calories >= 600:
            score += 20

    else:
        score += 10

    # -----------------------
    # Budget
    # -----------------------

    budget = user.get("daily_budget") or 0

    if price <= budget:
        score += 10

    # -----------------------
    # Restaurant Rating Bonus
    # -----------------------

    if rating >= 4.8:
        score += 10

    elif rating >= 4.5:
        score += 5

    return round(score, 2)