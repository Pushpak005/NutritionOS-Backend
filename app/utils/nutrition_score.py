"""
NutritionOS
Nutrition Score Engine v1.0
"""


def calculate_score(dish):

    protein = float(dish.get("protein") or 0)
    calories = float(dish.get("calories") or 0)
    fat = float(dish.get("fat") or 0)
    fiber = float(dish.get("fiber") or 0)
    rating = float(dish.get("rating") or 0)

    score = 0

    # Protein
    score += min(protein * 1.5, 35)

    # Fiber
    score += min(fiber * 2, 20)

    # Restaurant Rating
    score += rating * 5

    # Calories Penalty
    if calories > 650:
        score -= 8
    elif calories > 500:
        score -= 4

    # Fat Penalty
    if fat > 25:
        score -= 10
    elif fat > 15:
        score -= 5

    score = max(0, min(round(score), 100))

    return score


def recommendation_reason(score):

    if score >= 90:
        return "Excellent nutritional choice"

    if score >= 75:
        return "Very healthy meal"

    if score >= 60:
        return "Balanced option"

    if score >= 40:
        return "Average nutritional quality"

    return "Occasional treat"