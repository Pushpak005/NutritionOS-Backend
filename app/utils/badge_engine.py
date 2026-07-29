# ==========================================
# Smart Badge Engine
# NutritionOS
# ==========================================

def generate_badges(dish: dict):

    badges = []

    protein = float(dish.get("protein", 0))
    calories = float(dish.get("calories", 0))
    fat = float(dish.get("fat", 0))
    fiber = float(dish.get("fiber", 0))
    rating = float(dish.get("rating", 0))

    # Protein

    if protein >= 40:
        badges.append("💪 High Protein")

    elif protein >= 30:
        badges.append("🏋 Protein Rich")

    # Calories

    if calories <= 350:
        badges.append("🔥 Low Calorie")

    elif calories >= 650:
        badges.append("⚡ Energy Dense")

    # Fiber

    if fiber >= 8:
        badges.append("🌾 High Fiber")

    # Fat

    if fat <= 10:
        badges.append("❤️ Heart Friendly")

    # Rating

    if rating >= 4.7:
        badges.append("⭐ Top Rated")

    return badges