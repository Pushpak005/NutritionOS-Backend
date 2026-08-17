from sqlalchemy import text

from app.database import engine


def recommend_meals(user_id: int):

    with engine.connect() as conn:

        # ==========================================
        # User Profile
        # ==========================================

        user = conn.execute(

            text("""
                SELECT

                    name,
                    goal,
                    diet_preferences,
                    daily_budget,
                    daily_calories,
                    daily_protein

                FROM users

                WHERE id = :id
            """),

            {
                "id": user_id
            }

        ).mappings().first()

        if not user:

            return {

                "remaining_calories": 0,

                "remaining_protein": 0,

                "recommendations": [],

                "ai_message": "User not found."

            }

        # ==========================================
        # Today's Nutrition
        # Source: meal_logs
        # ==========================================

        consumed = conn.execute(

            text("""
                SELECT

                    COALESCE(
                        SUM(calories),
                        0
                    ) AS calories,

                    COALESCE(
                        SUM(protein),
                        0
                    ) AS protein

                FROM meal_logs

                WHERE

                    user_id = :id

                    AND DATE(eaten_at) = CURRENT_DATE

            """),

            {
                "id": user_id
            }

        ).mappings().first()

        # ==========================================
        # Remaining Nutrition
        # ==========================================

        daily_calories = float(
            user["daily_calories"] or 0
        )

        daily_protein = float(
            user["daily_protein"] or 0
        )

        consumed_calories = float(
            consumed["calories"] or 0
        )

        consumed_protein = float(
            consumed["protein"] or 0
        )

        remaining_calories = max(

            0,

            daily_calories - consumed_calories

        )

        remaining_protein = max(

            0,

            daily_protein - consumed_protein

        )

        # ==========================================
        # Available Menu
        # ==========================================

        menu = conn.execute(

            text("""
                SELECT

                    id,
                    dish_name,
                    calories,
                    protein,
                    price,
                    is_veg

                FROM menu_items

                WHERE available = TRUE

            """)

        ).mappings().all()

    # ==========================================
    # Rank Meals
    # ==========================================

    recommendations = []

    diet_preferences = (
        str(user["diet_preferences"] or "")
        .strip()
        .lower()
    )

    for meal in menu:

        meal = dict(meal)

        meal_calories = float(
            meal["calories"] or 0
        )

        meal_protein = float(
            meal["protein"] or 0
        )

        meal_price = float(
            meal["price"] or 0
        )

        score = 0

        # ------------------------------------------
        # Fits Remaining Calories
        # ------------------------------------------

        if meal_calories <= remaining_calories:

            score += 40

        # ------------------------------------------
        # Fits Remaining Protein
        # ------------------------------------------

        if meal_protein <= remaining_protein:

            score += 30

        # ------------------------------------------
        # Fits Daily Budget
        # ------------------------------------------

        if meal_price <= float(
            user["daily_budget"] or 0
        ):

            score += 20

        # ------------------------------------------
        # Vegetarian Preference
        # ------------------------------------------

        if (

            "veg" in diet_preferences

            and meal["is_veg"]

        ):

            score += 10

        # ------------------------------------------
        # Recommendation
        # ------------------------------------------

        recommendations.append({

            "score": score,

            **meal

        })

    # ==========================================
    # Highest Score First
    # ==========================================

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    top_meals = recommendations[:3]

    # ==========================================
    # AI Message
    # ==========================================

    if top_meals:

        best = top_meals[0]

        ai_message = (

            f"Hi {user['name']} 👋\n\n"

            f"You still have "
            f"{remaining_calories:.0f} calories "

            f"and "
            f"{remaining_protein:.0f}g protein "
            f"remaining today.\n\n"

            f"My top recommendation is "
            f"'{best['dish_name']}'.\n\n"

            f"It contains "
            f"{float(best['protein'] or 0):.0f}g protein, "

            f"{float(best['calories'] or 0):.0f} kcal "

            f"and costs "
            f"₹{float(best['price'] or 0):.0f}.\n\n"

            f"This meal supports your "
            f"{user['goal']} goal "
            f"while staying within your "
            f"daily nutrition target."

        )

    else:

        ai_message = (

            "No suitable meal recommendations "
            "are available right now."

        )

    # ==========================================
    # Response
    # ==========================================

    return {

        "remaining_calories":
            remaining_calories,

        "remaining_protein":
            remaining_protein,

        "recommendations":
            top_meals,

        "ai_message":
            ai_message

    }