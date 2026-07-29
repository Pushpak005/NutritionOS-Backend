# ==========================================
# NutritionOS Health Engine
# ==========================================


def calculate_bmi(height_cm: float, weight_kg: float):

    if height_cm <= 0:
        return 0

    height_m = height_cm / 100

    bmi = weight_kg / (height_m * height_m)

    return round(bmi, 2)


# ==========================================


def bmi_category(bmi: float):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Healthy"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


# ==========================================


def calculate_bmr(

    gender,
    age,
    height_cm,
    weight_kg

):

    gender = gender.lower()

    if gender == "male":

        return round(

            10 * weight_kg
            +
            6.25 * height_cm
            -
            5 * age
            +
            5

        )

    return round(

        10 * weight_kg
        +
        6.25 * height_cm
        -
        5 * age
        -
        161

    )


# ==========================================


def calculate_tdee(

    bmr,
    activity_level

):

    activity = activity_level.lower()

    multipliers = {

        "sedentary": 1.20,

        "light": 1.375,

        "moderate": 1.55,

        "active": 1.725,

        "very active": 1.90

    }

    multiplier = multipliers.get(

        activity,

        1.55

    )

    return round(

        bmr * multiplier

    )


# ==========================================


def calculate_calorie_target(

    tdee,

    goal

):

    goal = goal.lower()

    if "loss" in goal:

        return round(tdee - 500)

    elif "gain" in goal:

        return round(tdee + 300)

    return round(tdee)


# ==========================================


def calculate_macros(

    calories,

    goal

):

    goal = goal.lower()

    if "gain" in goal:

        protein_percent = 0.30

        fat_percent = 0.25

    elif "loss" in goal:

        protein_percent = 0.35

        fat_percent = 0.25

    else:

        protein_percent = 0.25

        fat_percent = 0.25

    carb_percent = 1 - protein_percent - fat_percent

    protein = round(

        calories * protein_percent / 4

    )

    carbs = round(

        calories * carb_percent / 4

    )

    fat = round(

        calories * fat_percent / 9

    )

    fiber = round(

        calories / 1000 * 14

    )

    return {

        "daily_calories": calories,

        "daily_protein": protein,

        "daily_carbs": carbs,

        "daily_fat": fat,

        "daily_fiber": fiber

    }