from datetime import datetime


def get_current_meal_window():

    hour = datetime.now().hour

    if 5 <= hour < 11:

        return "Breakfast"

    if 11 <= hour < 16:

        return "Lunch"

    if 16 <= hour < 19:

        return "Snack"

    if 19 <= hour < 23:

        return "Dinner"

    return "Late Night"