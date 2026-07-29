# ==========================================
# AI Explanation Engine
# NutritionOS
# ==========================================

def generate_explanation(goal: str, dish: dict) -> str:

    goal = goal.lower()

    protein = float(dish.get("protein", 0))
    calories = float(dish.get("calories", 0))
    fat = float(dish.get("fat", 0))
    fiber = float(dish.get("fiber", 0))
    rating = float(dish.get("rating", 0))
    price = float(dish.get("price", 0))

    if goal == "muscle gain":

        return (
            f"Excellent for muscle gain with {protein:.0f} g protein, "
            f"{calories:.0f} kcal, only {fat:.0f} g fat, "
            f"rated {rating:.1f}★ and available for ₹{price:.0f}."
        )

    elif goal == "weight loss":

        return (
            f"Suitable for weight loss with {calories:.0f} kcal, "
            f"{protein:.0f} g protein, {fiber:.0f} g fiber "
            f"and only {fat:.0f} g fat."
        )

    else:

        return (
            f"A balanced meal containing {protein:.0f} g protein, "
            f"{fiber:.0f} g fiber and a restaurant rating of "
            f"{rating:.1f}★."
        )