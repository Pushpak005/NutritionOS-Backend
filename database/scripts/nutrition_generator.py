import random


MEAL_TYPES = [
    "Breakfast",
    "Lunch",
    "Dinner"
]

CATEGORIES = [
    "Bowl",
    "Wrap",
    "Meal",
    "Salad",
    "Plate",
    "Breakfast"
]

CUISINES = [
    "Healthy Indian",
    "Continental",
    "Mediterranean",
    "Mexican",
    "Asian",
    "Healthy"
]

SPICE_LEVELS = [
    "None",
    "Mild",
    "Medium"
]


def generate_nutrition():

    calories = random.randint(280, 780)

    protein = random.randint(18, 55)

    carbs = random.randint(18, 75)

    fat = random.randint(6, 28)

    fiber = random.randint(3, 12)

    price = random.choice([
        179,
        199,
        219,
        249,
        269,
        289,
        299,
        329,
        349,
        379
    ])

    healthy_score = random.randint(82, 99)

    popularity_score = random.randint(75, 99)

    prep_time = random.choice([
        10,
        15,
        18,
        20,
        25
    ])

    return {

        "category": random.choice(CATEGORIES),

        "meal_type": random.choice(MEAL_TYPES),

        "cuisine": random.choice(CUISINES),

        "calories": calories,

        "protein": protein,

        "carbs": carbs,

        "fat": fat,

        "fiber": fiber,

        "price": price,

        "healthy_score": healthy_score,

        "popularity_score": popularity_score,

        "prep_time": prep_time,

        "spice_level": random.choice(
            SPICE_LEVELS
        ),

        "available": True

    }