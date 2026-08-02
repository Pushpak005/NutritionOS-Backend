import math


# ==========================================
# BMI
# ==========================================

def calculate_bmi(height_cm: float, weight_kg: float) -> float:

    height_cm = float(height_cm)
    weight_kg = float(weight_kg)

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


# ==========================================
# BMR (Mifflin-St Jeor)
# ==========================================

def calculate_bmr(
    gender: str,
    age: int,
    height_cm: float,
    weight_kg: float
) -> float:

    height_cm = float(height_cm)
    weight_kg = float(weight_kg)

    gender = gender.lower()

    if gender == "male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    return round(bmr)


# ==========================================
# Activity Multiplier
# ==========================================

def get_activity_multiplier(activity_level: str):

    activity_level = activity_level.lower()

    mapping = {

        "sedentary": 1.2,

        "light": 1.375,

        "moderate": 1.55,

        "active": 1.725,

        "very active": 1.9,

        # Frontend values
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.9
    }

    return mapping.get(activity_level, 1.55)


# ==========================================
# TDEE
# ==========================================

def calculate_tdee(
    bmr: float,
    activity_level: str
):

    multiplier = get_activity_multiplier(activity_level)

    return round(
        bmr * multiplier
    )


# ==========================================
# Calories based on Goal
# ==========================================

def calculate_daily_calories(
    tdee: float,
    goal: str
):

    goal = goal.lower()

    if "loss" in goal:

        return tdee - 500

    elif "gain" in goal:

        return tdee + 300

    else:

        return tdee


# ==========================================
# Macros
# ==========================================

def calculate_macros(
    calories: int,
    weight_kg: float
):

    calories = float(calories)
    weight_kg = float(weight_kg)

    protein = round(weight_kg * 1.8)

    fat = round((calories * 0.25) / 9)

    protein_calories = protein * 4

    fat_calories = fat * 9

    carbs = round(
        (
            calories
            - protein_calories
            - fat_calories
        ) / 4
    )

    fiber = 30

    return {

        "protein": protein,

        "fat": fat,

        "carbs": carbs,

        "fiber": fiber
    }


# ==========================================
# Complete Nutrition Engine
# ==========================================

def calculate_nutrition(profile: dict):

    bmi = calculate_bmi(
        profile["height_cm"],
        profile["weight_kg"]
    )

    bmr = calculate_bmr(
        profile["gender"],
        profile["age"],
        profile["height_cm"],
        profile["weight_kg"]
    )

    tdee = calculate_tdee(
        bmr,
        profile["activity_level"]
    )

    calories = calculate_daily_calories(
        tdee,
        profile["goal"]
    )

    macros = calculate_macros(
        calories,
        profile["weight_kg"]
    )

    print("===== NUTRITION ENGINE =====")
    print(profile)
    print("BMI:", bmi)
    print("BMR:", bmr)
    print("TDEE:", tdee)
    print("Calories:", calories)
    print(macros)
    print("============================")

    return {

        "bmi": bmi,

        "bmr": bmr,

        "tdee": tdee,

        "daily_calories": calories,

        "daily_protein": macros["protein"],

        "daily_carbs": macros["carbs"],

        "daily_fat": macros["fat"],

        "daily_fiber": macros["fiber"]
    }