def get_meal_target_calories(
    daily_calories: int,
    meal: str
):

    meal = meal.lower()

    if meal == "breakfast":
        return round(daily_calories * 0.25)

    if meal == "lunch":
        return round(daily_calories * 0.35)

    if meal == "dinner":
        return round(daily_calories * 0.30)

    if meal == "snack":
        return round(daily_calories * 0.10)

    return daily_calories