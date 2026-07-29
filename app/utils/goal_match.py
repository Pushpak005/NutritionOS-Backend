# ==========================================
# Goal Match Engine
# NutritionOS
# ==========================================


def calculate_goal_match(goal: str, dish: dict) -> int:

    goal = goal.lower()

    protein = float(dish.get("protein", 0))
    calories = float(dish.get("calories", 0))
    fat = float(dish.get("fat", 0))
    fiber = float(dish.get("fiber", 0))
    rating = float(dish.get("rating", 0))

    score = 0

    # ======================================
    # MUSCLE GAIN
    # ======================================

    if goal == "muscle gain":

        score += min(protein * 1.2, 50)

        if 300 <= calories <= 700:
            score += 20
        elif calories > 700:
            score += 10

        if fat <= 15:
            score += 10

        score += min(fiber, 10)

        score += rating * 2

    # ======================================
    # WEIGHT LOSS
    # ======================================

    elif goal == "weight loss":

        if calories <= 350:
            score += 40
        elif calories <= 500:
            score += 25
        else:
            score += 10

        score += min(protein, 30)

        score += min(fiber * 2, 20)

        if fat <= 10:
            score += 10

    # ======================================
    # GENERAL HEALTH
    # ======================================

    else:

        score += min(protein, 30)

        score += min(fiber * 2, 20)

        if calories <= 500:
            score += 20

        if fat <= 15:
            score += 15

        score += rating * 3

    return min(round(score), 100)


# ==========================================
# Goal Match Label
# ==========================================

def goal_match_label(match: int) -> str:

    if match >= 90:
        return "Excellent Match"

    elif match >= 75:
        return "Strong Match"

    elif match >= 60:
        return "Good Match"

    elif match >= 40:
        return "Average Match"

    return "Weak Match"