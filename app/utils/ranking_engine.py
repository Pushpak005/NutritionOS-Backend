# ==========================================
# NutritionOS Ranking Engine
# ==========================================

def calculate_final_score(dish: dict) -> float:

    nutrition = float(dish.get("nutrition_score", 0))
    goal = float(dish.get("goal_match", 0))
    rating = float(dish.get("rating", 0))
    delivery = float(dish.get("delivery_time", 30))

    score = 0

    # Nutrition
    score += nutrition * 0.40

    # Goal Match
    score += goal * 0.40

    # Restaurant Rating
    score += rating * 4

    # Faster delivery bonus
    score += max(0, 30 - delivery)

    return round(score, 2)