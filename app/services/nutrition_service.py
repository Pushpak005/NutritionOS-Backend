def calculate_nutrition(
    gender,
    age,
    height_cm,
    weight_kg,
    activity_level,
    goal,
):
    """
    Calculates BMI, BMR, TDEE,
    Calories, Protein, Carbs,
    Fat and Fiber.
    """

    # -------------------------
    # BMI
    # -------------------------

    height_m = height_cm / 100

    bmi = round(
        weight_kg / (height_m * height_m),
        2
    )

    # -------------------------
    # BMR
    # Mifflin-St Jeor
    # -------------------------

    if gender.lower() == "male":

        bmr = (
            10 * weight_kg +
            6.25 * height_cm -
            5 * age +
            5
        )

    else:

        bmr = (
            10 * weight_kg +
            6.25 * height_cm -
            5 * age -
            161
        )

    # -------------------------
    # Activity Multiplier
    # -------------------------

    activity_map = {

        "Sedentary": 1.2,

        "Lightly Active": 1.375,

        "Moderately Active": 1.55,

        "Very Active": 1.725,

        "Extra Active": 1.9,
    }

    multiplier = activity_map.get(
        activity_level,
        1.2
    )

    tdee = bmr * multiplier

    # -------------------------
    # Goal
    # -------------------------

    if goal.lower() == "weight loss":

        calories = tdee - 500

    elif goal.lower() == "weight gain":

        calories = tdee + 300

    else:

        calories = tdee

    calories = round(calories)

    # -------------------------
    # Macros
    # -------------------------

    protein = round(weight_kg * 1.8)

    fat = round((calories * 0.25) / 9)

    carbs = round(
        (
            calories
            - (protein * 4)
            - (fat * 9)
        ) / 4
    )

    fiber = 30

    return {

        "bmi": bmi,

        "bmr": round(bmr),

        "tdee": round(tdee),

        "daily_calories": calories,

        "daily_protein": protein,

        "daily_carbs": carbs,

        "daily_fat": fat,

        "daily_fiber": fiber,
    }